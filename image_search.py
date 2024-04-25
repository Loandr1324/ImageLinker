# Author Loik Andrey mail: loikand@mail.ru
import yadisk
from loguru import logger
from config import YA_TOKEN, FILE_NAME_LOG_SEARCH, FILE_NAME_IMAGE_LINK, FOLDER_YA_IMAGE
from data.csv_work import WorkCSV

# Задаём параметры логирования
logger.add(FILE_NAME_LOG_SEARCH,
           format="{time:DD/MM/YY HH:mm:ss} - {file} - {level} - {message}",
           level="INFO",
           rotation="1 week",
           compression="zip")


def list_images_in_public_folder(y: yadisk.client.Client, path: str, public_url_base: str, list_url: list) -> None:
    try:
        # Получаем список всех элементов в текущей директории
        items = y.listdir(path)

        for item in items:
            # Полный путь к текущему элементу
            item_path = f"{path}/{item.name}".replace("//", "/")

            if item.type == "dir":
                # Если элемент является директорией, рекурсивно вызываем функцию
                list_images_in_public_folder(y, item_path, public_url_base, list_url)

            elif item.type == "file" and item.media_type == "image":
                # Формируем путь для вывода
                path1 = item_path.split('/IM_images/', 1)[1].split('/')
                brand_name = path1[0]
                filename = path1[1]
                number = filename.split('.')[0]
                logger.debug(f"{brand_name=}, {number=}")
                display_path = f"{public_url_base}/{item_path.split('/IM_images/', 1)[1]}"
                abcp_path = f"{public_url_base}/{brand_name}/{filename}".replace("/", "\/")

                # Выводим информацию о файле
                logger.debug(f"Путь: {display_path}")
                logger.debug(f"Путь ABCP: {abcp_path}")
                list_url.append({'brand_name': brand_name,'number': number, 'url': display_path, 'url_abcp': abcp_path})

    except Exception as e:
        logger.error(f"Ошибка при доступе к {path}: {e}")


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
            url_abcp=item['url_abcp'],
            type_data='image_link'
        )
    wk_csv.add_data_file()


def run():

    y = yadisk.YaDisk(token=YA_TOKEN)  # smart
    list_url = []
    # Проверяем, подключены ли мы к Яндекс.Диску
    if y.check_token():
        logger.info("Авторизация прошла успешно!")
        # Получаем метаданные папки IM_images
        meta = y.get_meta(FOLDER_YA_IMAGE)

        if not meta.public_url:
            logger.error("Подумай над тем, чтобы сделать эту папку публичной")
            # # Если папка не является публичной, делаем её публичной
            # y.publish("/IM_images")
            # # Обновляем метаданные после публикации
            # meta = y.get_meta("/IM_images")
        else:
            # Вызываем функцию для публичной папки FOLDER_YA_IMAGE
            list_images_in_public_folder(y, FOLDER_YA_IMAGE, meta.public_url, list_url)
            save_csv(list_url)
    else:
        logger.error("Ошибка авторизации")


if __name__ == '__main__':
    run()
