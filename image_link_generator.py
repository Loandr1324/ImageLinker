# Author Loik Andrey mail: loikand@mail.ru
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from loguru import logger
from config import FILE_NAME_LOG_LINK, FILE_NAME_IMAGE_LINK
from data.csv_work import WorkCSV

# Задаём параметры логирования
logger.add(FILE_NAME_LOG_LINK,
           format="{time:DD/MM/YY HH:mm:ss} - {file} - {level} - {message}",
           level="INFO",
           rotation="1 week",
           compression="zip")

app = Flask(__name__)
CORS(app)

@app.route('/multifinderbrands.py', methods=['POST'])
def get_image_links():
    # Проверяем тип содержимого запроса и извлекаем данные соответствующим образом
    if request.content_type == 'application/json':
        data = request.get_json()
        if not data:
            logger.error("Empty request data")
            abort(400, description="Bad Request: No data provided")
    elif request.content_type == 'application/x-www-form-urlencoded':
        data = [request.form]  # Оборачиваем form dict в список для унификации обработки
    else:
        abort(400, description="Unsupported Media Type")

    # Получаем данные из базы данных по существующим ссылкам
    wk_csv = WorkCSV(FILE_NAME_IMAGE_LINK)

    # Формируем ответ на POST запрос из имеющихся данных
    response = []
    for item in data:
        brand = item.get('brand')
        article = item.get('article')

        # Если в JSON нет необходимых ключей, то возвращаем ошибку
        if not brand or not article:
            logger.error("Missing brand or article in request")
            continue

        # Фильтруем имеющиеся данные по полученным параметрам
        list_image = wk_csv.filter(brand=brand, article=article, type_filter='image_link')

        # Если данные есть добавляем их в ответ на запрос
        if list_image:
            for image in list_image:
                # Т.к. в базе может быть несколько вариантов с одним брендом артикулом, то выбираем точное соответствие
                number = image.get('number', '').split("_")
                if article == number[0]:
                    response.append({"url": image['url_abcp']})

        # Если данных нет, то возвращаем ошибку
        else:
            logger.info(f"No images found for brand: {brand}, article: {article}")
            abort(404, description="Images not found")

    # Если ответ не сформирован, то возвращаем ошибку
    if not response:
        abort(404, description="No matching images found for any items")

    return jsonify(response)


if __name__ == '__main__':
    app.run()
