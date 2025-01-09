from datetime import date
import pydantic

from dars import datastructs as ds
from dars import (
        config,
        defaults,
        errors,
        )


class AppModel(pydantic.BaseModel):
    settings: config.Settings | None = None
    base: ds.Base = ds.Base.FZ44
    upload: bool = True
    # --- задержка перед скачиваен документов по ссылкам, полученным
    #     в запросе
    #     Если выполнять скачивание сразу после запроса, то выдается 404,
    #     т.е. архивы не успевают сформироваться
    delay_before_download: int = defaults.DELAY_BEFORE_DOWNLOAD
    prefix: str = ''
    # --- дополнительный путь (или суффик) к директории сохранения файла
    #     в файловой системе (download_dir)
    download_dir_suffix: str = ''
    # --- замена имени загружаемого файла
    #     СОИ к каждому имени файла может добалять временнУю отметку,
    #     что нарушает работу кеширования
    #     filename_substitute позволяет вырезать эту метку через re
    #     Использование:
    #         re.sub(filename_substitute, '', filename)
    filename_substitute: str | None = None

    @property
    def base_settings(self) -> pydantic.BaseModel:
        '''Получить текущую конфигурацию для base'''
        if not self.settings:
            raise errors.SettingsUndefinedError
        if self.base == ds.Base.FZ44:
            return self.settings.fz44
        if self.base == ds.Base.FZ223:
            return self.settings.fz223
        if self.base == ds.Base.PPRF615:
            return self.settings.pprf615
        raise NotImplementedError


class GetNsiRequestModel(AppModel):
    '''Параметры запроса справочника'''
    nsiCode: str
    nsiKind: ds.NsiKind = ds.NsiKind.ALL


class OrganizationModel(pydantic.BaseModel):
    '''Параметры организации'''
    inn: str
    kpp: str
    ogrn: str | None = None


class GetPublicDocsRequestModel(AppModel):
    '''Параметры запроса публичных документов'''
    subsystemtype: str
    regnums: list[str] = []
    organizations: list[OrganizationModel] = []
    monthinfo: date | None = None
    exactdate: date | None = None
    todayinfo: str | None = pydantic.Field(default=None, pattern=r'^\d+-\d+$')
    offsettimezone: str = defaults.TZ
    jobs: int = 1

    @pydantic.computed_field
    def fromhour(self) -> int:
        if self.todayinfo:
            return int(self.todayinfo.split('-')[0])

    @pydantic.computed_field
    def tohour(self) -> int:
        if self.todayinfo:
            return int(self.todayinfo.split('-')[1])


class GetDocsByReestrNumberRequestModel(AppModel):
    '''Параметры запроса публичных документов'''
    subsystem_type: str
    reestr_number: str
    jobs: int = 1


class GetDocsByOrgRegionRequestModel(AppModel):
    subsystem_type: str
    region: int
    document_type: str
    reestr_number: str | None = None
    target_date: date = date.today()
    timezone: str = defaults.TZ
    jobs: int = 1
    # --- флаг обработки ссылок
    #     для реализации раздельного механизма получения и обработки
    #     ссылок флаг поставить в False
    process_response_links: bool = True

    @pydantic.computed_field
    def exact_date(self) -> str:
        td = self.target_date.strftime('%Y-%m-%d')
        return f'{td}{self.timezone}'

    @pydantic.computed_field
    def kladr_region(self) -> str:
        return str(self.region).rjust(2, '0')
