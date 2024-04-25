# ImageLinker
В данном проекте расположена два скрипта
[image_link_generator.py](image_link_generator.py) - скрипт на Flask для возврата ответа на 
POST запросы
Скрипт в ответ на POST-запрос деталью должен возвращать JSON-ответ 
со списком всех изображений к товару, отправленному в запросе.
[image_search.py](image_search.py) - скрипт, который получает данный с Яндекс.Диск и 
записывает их в базу данных.

### Описание

------------
В данном проекте расположена два скрипта
[image_link_generator.py](image_link_generator.py) - скрипт на Flask для возврата ответа на 
POST запросы
Скрипт в ответ на POST-запрос деталью должен возвращать JSON-ответ 
со списком всех изображений к товару, отправленному в запросе.
````
ЗАПРОС (POST):
URL:  http://server_name//multifinderbrands.php
BODY: 
[
   {
  	"brand": "febi",
  	"article": "01089"
   }
]

ОТВЕТ:
[
  {
    "url": "https:\/\/server_name\/febi\/01089.jpg"
  },
  {
    "url": "https:\/\/server_name\/febi\/01089_1.jpg"
  }
]
````
[image_search.py](image_search.py) - скрипт, который получает данные с Яндекс.Диск и 
записывает их в базу данных на этом сервере для оптимизации скорости ответа на POST запросы.
Для работы с Яндекс.Диск требуется создать приложения и получить токен на Яндекс.

[Инструкция по получению ТОКЕНа](https://snipp.ru/php/disk-yandex)

[Регистрация приложения в Ядекс.Диск.docx](%D0%E5%E3%E8%F1%F2%F0%E0%F6%E8%FF%20%EF%F0%E8%EB%EE%E6%E5%ED%E8%FF%20%E2%20%DF%E4%E5%EA%F1.%C4%E8%F1%EA.docx)

### Доступы

------------
Данные для доступа скрипта размещаем в файл config.py:  
```python
YA_TOKEN: str = 'ваш токен Яндекс приложения'
FILE_NAME_LOG_LINK: str = 'имя фала лога для работы скрипта image_link_generator.py'
FILE_NAME_LOG_SEARCH: str = 'имя фала лога для работы скрипта image_link_generator.py'
FILENAME_IMAGE_LINK: str = 'путь относительно корневой директории до файла БД'
FOLDER_YA_IMAGE: str = 'папка для поиска изображений на Яндекс.Диск'
```

### Примечание 

------------
Для логирования используется библиотека [logguru](https://loguru.readthedocs.io/en/stable/overview.html)
Наименование лог файла прописывается в файле config.py в переменные `FILE_NAME_LOG_LINK` 
и `FILE_NAME_LOG_SEARCH`