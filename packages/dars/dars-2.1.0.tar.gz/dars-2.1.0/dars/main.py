'''Входная точка бизнес-логии модуля'''

import os
import logging
import requests
import time
import re
import threading

import xml.dom.minidom
import xml.parsers.expat

from concurrent import futures

from dars import (
        config,
        errors,
        getnsirequest,
        getdocsbyreestrnumberrequest,
        getdocsbyorgregionrequest,
        models,
        s3_repo,
        utils,
        )

logger = logging.getLogger('dars')

REQUEST_RETRIES = 5

TRIM_REQUEST_LOG = 4096
TRIM_RESPONSE_LOG = 4096


class Client:
    '''Клинетский класс для доступа к бизнес-логике'''

    def __init__(self, settings: config.Settings):
        self.settings = settings
        self.repo = s3_repo.S3Repo(self.settings.s3)
        # --- индекс обработанных файлов
        self.filename_index = {}
        self.lock = threading.Lock()

    def getNsiRequest(self, **kwargs):
        '''Загрузить справочники НСИ'''
        self.params = models.GetNsiRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getnsirequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return
        for (_, url) in getnsirequest.extract_archive_info(response_text):
            self._process_response_link(url, upload=self.params.upload)

    def getDocsByReestrNumberRequest(self, **kwargs) -> list[str]:
        '''Запрос архивов с документами по реестровому номеру

        Args:
            kwargs - параметры для формирования модели
                     GetDocsByOrgRegionRequestModel

        Returns:
            Список файлов в файловой системе
        '''
        self.params = models.GetDocsByReestrNumberRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getdocsbyreestrnumberrequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return
        # ---
        urls = getdocsbyreestrnumberrequest.extract_archive_info(
                response_text,
                )
        return self._process_response_links(
                urls,
                upload=self.params.upload
                )

    def getDocsByOrgRegionRequest(self, **kwargs) -> list[str]:
        '''Запрос архивов по региону заказчика и типу документа'''
        self.params = models.GetDocsByOrgRegionRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getdocsbyorgregionrequest.render(self.params)
        response_text = self._make_request(body)
        if not response_text:
            return []
        # ---
        urls = getdocsbyorgregionrequest.extract_archive_info(
                response_text,
                )
        if not self.params.process_response_links or not urls:
            return urls
        self._process_response_links(
                urls,
                self.params.upload
                )
        return urls

    def _process_response_links(
            self,
            urls: list[str | tuple[str]],
            upload: bool = False
            ):
        '''Обработать ссылки из СОИ

        Данный метод загружает файлы по ссылкам, полученным из СОИ.

        Args:
            urls - список ссылок, полученных из СОИ или список пар
                ссылка / prefix
            upload - флаг выгрузки в S3

        Returns:
            Список имен файлов в файловой системе
        '''
        if not urls:
            return
        time.sleep(self.params.delay_before_download)
        if self.params.jobs == 1:
            for url in urls:
                if isinstance(url, str):
                    self._process_response_link(
                            url=url,
                            upload=self.params.upload
                            )
                else:
                    self._process_response_link(
                            url=url[0],
                            prefix=url[1],
                            upload=self.params.upload
                            )
        else:
            with futures.ThreadPoolExecutor(
                    max_workers=self.params.jobs
                    ) as executor:
                for url in urls:
                    if isinstance(url, str):
                        executor.submit(
                                self._process_response_link,
                                url=url,
                                upload=upload
                                )
                    else:
                        executor.submit(
                                self._process_response_link,
                                url=url[0],
                                prefix=url[1],
                                upload=upload
                                )

    def _process_response_link(
            self,
            url: str,
            prefix: str | None = None,
            upload: bool = False
            ) -> str:
        '''Обработать ссылку из СОИ

        Ссылка, полученная из СОИ, указывает на архив документов.
        Му получаем имя файла, проверяем наличие файла в ФС и S3,
        загружаем файл в S3

        Args:
            url - ссылка
            upload - выгружаем полученные файлы в S3

        Returns:
            полный путь к файлу в файловой системе
        '''
        filename = self._get_remote_filename(url)
        if not filename:
            return
        # --- обрезаем лишнее
        if self.params.filename_substitute:
            filename = re.sub(
                    self.params.filename_substitute,
                    '',
                    filename
                    )
        # --- проверяем на дублирование имени файла
        filename = self._correct_duplication(filename)
        # --- проверяем существование файла в S3 (только при условии,
        #     что файл надо выгружать в S3)
        prefix = prefix or self.params.prefix
        if upload:
            if self.repo.exists(filename, prefix=prefix):
                logger.info(
                        '           %s уже существует, пропускаем.',
                        os.path.join(prefix, filename)
                        )
                return
        # --- проверяем существование файла в файловой системе
        download_dir = os.path.join(
                self.params.base_settings.download_dir,
                self.params.download_dir_suffix
                )
        file_path = os.path.join(download_dir, filename)
        if os.path.exists(file_path):
            pass
        else:
            # --- загружаем файл из СОИ в ФС
            self._download_file(url, file_path)
        # ---
        if not os.path.exists(file_path):
            logger.error(f'Ошибка сохранения файла {file_path}')
            return
        size = utils.humanize_size(os.path.getsize(file_path))
        logger.info('%10s %s/%s', size, prefix, filename)
        # --- выгружаем файл из ФС в S3
        if upload:
            self.repo.put_file(file_path, prefix=prefix)
        # ---
        return file_path

    def _make_request(self, body: str) -> str:
        '''Выполнить запрос к СОИ

        Args:
            body - тело запроса
        Returns:
            Текст ответа
        '''
        logger.debug(
                'Выполнение запроса на %s',
                self.params.base_settings.url
                )
        logger.debug(utils.truncate_string(body, TRIM_REQUEST_LOG))
        response = self._make_repeated_request(
                'POST',
                url=self.params.base_settings.url,
                data=body,
                timeout=60
                )
        logger.debug('HTTP код ответа: %s', response.status_code)
        logger.debug(response.headers)
        try:
            logger.debug(
                    utils.truncate_string(
                        xml.dom.minidom.parseString(
                            response.text
                            ).toprettyxml(),
                        TRIM_RESPONSE_LOG
                        )
                    )
        except xml.parsers.expat.ExpatError as e:
            logger.error(e)
            logger.debug(response.text)
        # ---
        if response.status_code != 200:
            logger.error(
                    'СОИ вернул неожиданный статус ответа '
                    f'{response.status_code}'
                    )
            logger.error(response.text)
            return None
        return response.text

    def _download_file(self, url: str, file_path: str) -> str:
        '''Скачать файл

        Args:
            url - ссылка для скачивания
            file_path - полный путь к файлу
        Return:
            Полный путь файла в файловой системе
        raises:
            EisClientUnexpectedStatus - СОИ вернул не 200
        '''
        download_dir = os.path.dirname(file_path)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        # ---
        response = self._make_repeated_request(
                'GET',
                url=url,
                timeout=60
                )
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
        raise errors.EisClientUnexpectedStatus(response.status_code)

    def _get_remote_filename(self, url: str) -> str:
        '''Получить имя файла без скачивания'''
        response = self._make_repeated_request(
                'HEAD',
                url=url,
                timeout=60
                )
        code = response.status_code
        if code != 200:
            logger.error(f'Неожиданный статус при запросе имени файла {code}')
            logger.error(response.text)
            logger.error(url)
            return None
        content_disposition = response.headers.get('content-disposition')
        if not content_disposition:
            logger.error(f'Ошибка при получении имени файла {url}')
            return None
        filename = content_disposition.split('=')[1][1:-1]
        return filename

    def _correct_duplication(self, filename: str) -> str:
        '''Скорректировать имя файла с учетом возможного дублирования

        В рамках одной сессии могут быть получены одинаковые имена файлов
        с различным содержанием. Необходимо вести учет обработанных файлов
        и индекс повторяемости. В случае дублирования, индекс увеличивается
        на единицу и добавляется в имя
        filename.zip
        filename_2.zip
        filename_3.zip
        '''
        with self.lock:
            index = self.filename_index.get(filename)
            if not index:
                self.filename_index[filename] = 1
                return filename
            index = index + 1
            self.filename_index[filename] = index
            base_name, extension = os.path.splitext(filename)
            new_filename = base_name + '_' + str(index).zfill(2) + extension
            return new_filename

    def _make_repeated_request(self, verb: str, **kwargs
                               ) -> requests.Response | None:
        '''Выполнить запрос с повтором при ошибке'''
        # --- выполняем подмену префикса, если задана соответствующая
        #     конфигурация
        if self.params.settings.url_prefix_substitution:
            for sub_item in self.params.settings.url_prefix_substitution:
                if kwargs['url'].startswith(sub_item['source']):
                    kwargs['url'] = re.sub(
                            '^' + sub_item['source'],
                            sub_item['dest'],
                            kwargs['url']
                            )
                    break
        # ---
        if self.settings.token:
            headers = kwargs.get('headers', {})
            headers['individualPerson_token'] = self.settings.token
            kwargs['headers'] = headers
        for _ in range(REQUEST_RETRIES):
            try:
                resp = requests.request(
                        verb,
                        **kwargs,
                        )
                resp.raise_for_status()
                return resp
            except (
                    requests.exceptions.HTTPError,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError
                    ) as e:
                logger.error(e)
                last_exception = e
                time.sleep(5)
        raise last_exception
