# Author Loik Andrey mail: loikand@mail.ru
import os
from loguru import logger
from config import YA_TOKEN, FILE_NAME_LOG_SEARCH, FILE_NAME_IMAGE_LINK, FOLDER_YA_IMAGE
from data.csv_work import WorkCSV

# Задаём параметры логирования
logger.add(FILE_NAME_LOG_SEARCH,
           format="{time:DD/MM/YY HH:mm:ss} - {file} - {level} - {message}",
           level="INFO",
           rotation="1 week",
           compression="zip")


def list_images_in_local_folder(base_url: str, local_path: str, list_url: list) -> None:
    try:
        # Проходим по всем файлам в директории и поддиректориях
        for root, dirs, files in os.walk(local_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, local_path)
                    brand_name = relative_path.split(os.sep)[0]
                    number = os.path.splitext(file)[0]
                    url = f"{base_url}/{brand_name}/{file}"
                    logger.debug(f"Brand: {brand_name}, Number: {number}, URL: {url}")
                    list_url.append({'brand_name': brand_name, 'number': number, 'url': url})
    except Exception as e:
        logger.error(f"Ошибка при доступе к {local_path}: {e}")


def save_csv(url_list: list[dict]) -> None:
    """
    Записываем данные в csv файл
    :param url_list: Список словарей с ключами [{'brand_name', 'number', 'url', 'url_abcp'}]
    :return: None
    """
    wk_csv = WorkCSV(FILE_NAME_IMAGE_LINK)
    for item in url_list:
        wk_csv.add_to_data(
            brand=item['brand_name'],
            number=item['number'],
            url=item['url'],
            type_data='image_link'
        )
    wk_csv.add_data_file()


def run():
    list_url = []
    base_url = "https://img.smart-a.ru/images"
    # list_images_in_local_folder(base_url, "C:\\srv\\images", list_url)  # для Windows
    list_images_in_local_folder(base_url, "/srv/images/", list_url)  # для Ubuntu
    save_csv(list_url)


if __name__ == '__main__':
    run()
