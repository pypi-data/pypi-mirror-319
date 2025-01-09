# Клиент для сервиса отдачи информации и документов ЕИС

Сервис отдачи информации и документов (СОИ) - это сервис для доступа к документам, размещенным в единой информационной системе (ЕИС) в сфере закупок [https://zakupki.gov.ru](https://zakupki.gov.ru).

Описание взаимодействия приведено в разделе 2.9.20 документа ЕИС Альбом ТФФ 15 ([ссылка](https://zakupki.gov.ru/epz/main/public/document/view.html?searchString=&sectionId=432&strictEqual=false)).

Данный проект является клиентской библиотекой для взаимодействия с СОИ.

Реализованные методы:
* getNsiRequest – запрос в хранилище документов (ХД) данных справочника
* getDocsByReestrNumberRequest – запрос формирования в ХД архивов с документами по реестровому номеру
* getDocsByOrgRegionRequest - запрос архивов по региону заказчика и типу документа

Файлы загружаются из СОИ в файловую систему или S3.

## Подготовка к работе

Перед началом использования клиента Вам понадобится *персональный токен*.
Токен можно получить после регистрации в ЕИС в соответствии с разделом 3
инструкции *docs/Инструкция_по_использованию_сервисов_отдачи_информации_с_регистрацией.pdf*.

## Установка и конфигурация

Установка

```bash
pip install dars
```

Конфигурация

```bash
# --- создать или отредактировать файл конфигурации
#     здесь обязательно указываем персональный токен (см. выше)
dars config edit
```

Пример файла конфигурации (~/.config/dars/config.toml)

```toml
token = "secret"

[fz44]
# --- адрес для запросов
#     по-умолчанию - тестовый сервис
# url = 'https://int44.zakupki.gov.ru/eis-integration/services/getDocsIP'
# --- директория для загрузки файлов из СОИ
# download_dir = "/tmp/dars/fz44/downloads"

[fz223]
# url = 'https://int44.zakupki.gov.ru/eis-integration/services/getDocsIP'
# # --- директория для загрузки файлов из СОИ
# download_dir = "/tmp/dars/fz223/downloads"


[s3]
# access_key = "user"
# secret_key = "superseret"
# endpoint_url = "http://localhost:9001"
# bucket = "my-bucket"
# region = "ru-1"
```

## Загрузка файлов

По умолчанию, файлы загружаются в S3 и копии остаются в директории загрузки файловой системы.
Директория загрузки задается параметром `download_dir`.
Доступ к S3 осуществляется в соовтетствии с секцией `[s3]`.

Для отмены загрузки файлов в S3 в командах необходимо указать опцию `--no-upload`.

## Примеры

Загрузка справочников

```bash
# --- загрузить список справочников по 44-ФЗ
dars getnsirequest \
  --base=fz44  \
  --nsicode=nsiAllList \
  --prefix=nsi/fz44

# --- загрузить справочник организаций по 44-ФЗ
dars getnsirequest \
  --base=fz44  \
  --nsicode=nsiOrganization \
  --prefix=nsi/fz44/nsiOrganization

# --- загрузить справочник типов документов по 44-ФЗ
dars getnsirequest \
  --base=fz44  \
  --nsicode=nsiDocumentTypes \
  --prefix=nsi/fz44/nsiDocumentType

# --- загрузить справочник организаций по 223-ФЗ
dars getnsirequest \
  --base=fz223 \
  --nsicode=nsiOrganization \
  --prefix=nsi/fz223/nsiOrganization

# --- загрузить справочник типов документов по 223-ФЗ
dars getnsirequest \
  --base=fz223  \
  --nsicode=nsiDocumentTypes223 \
  --prefix=nsi/fz223/nsiDocumentType
```

Запрос документов по реестровому номеру

```bash
# --- запрос плана-графика закупок по 44-ФЗ
dars getdocsbyreestrnumberrequest \
  --subsystem-type=RPGZ \
  --reestr-number=202403732000688001 \
  --prefix=public/fz44/tenderplans

# --- Запрос закупки по 44-ФЗ
dars getdocsbyreestrnumberrequest \
  --subsystem-type=PRIZ \
  --reestr-number=0338100003724000064 \
  --prefix=public/fz44/purchases
```

## Использование в качестве модуля

```python
import dars

s3 = {
    "access_key": "key",
    "secret_key": "secret",
    "endpoint_url": "http://localhost:9002",
    "bucket": "drs",
    "region": "ru-1"
}
client = dars.client(sender='myapp', s3=s3)

keys = client.getNsiRequest(
                base='fz44',
                nsicode='nsiOrganization',
                prefix='fz44/nsi/nsiOrganization'
                )
```

## Типы подсистем и документов

Типы подсистем и документов, используемых в аргументах команды, приведены
в приложениях 1 и 2 инструкции *docs/Инструкция_по_использованию_сервисов_отдачи_информации_с_регистрацией.pdf*
