# Author Loik Andrey mail: loikand@mail.ru
from flask import Flask, request, jsonify, abort, Response, render_template, flash, redirect
import json
from flask_cors import CORS
from loguru import logger
from config import FILE_NAME_LOG_LINK, FILE_NAME_IMAGE_LINK, SECRET_KEY
from data.csv_work import WorkCSV
from forms import LoginForm

# Задаём параметры логирования
logger.add(FILE_NAME_LOG_LINK,
           format="{time:DD/MM/YY HH:mm:ss} - {file} - {level} - {message}",
           level="INFO",
           rotation="1 week",
           compression="zip")

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/multifinderbrands.py', methods=['POST'])
def get_image_links():
    # Проверяем тип содержимого запроса и извлекаем данные соответствующим образом
    if request.content_type == 'application/json':
        data = request.get_json()
        if not data:
            logger.error("Empty request data")
            abort(400, description="Bad Request: No data provided")
    elif request.content_type == 'application/x-www-form-urlencoded':
        # Если полученные данные не являются словарём, то преобразуем ключ в json
        if request.form.get('brand'):
            data = [request.form]  # Оборачиваем form dict в список для унификации обработки
        else:
            keys_str = list(request.form.keys())[0]
            data = json.loads(keys_str)
        if not data:
            logger.error("Empty request data")
            abort(400, description="Bad Request: No data provided")
    else:
        abort(400, description="Unsupported Media Type")

    logger.debug(f"Поступили параметры: {data=}")

    # Получаем данные из базы данных по существующим ссылкам
    wk_csv = WorkCSV(FILE_NAME_IMAGE_LINK)

    # Формируем ответ на POST запрос из имеющихся данных
    response = []
    for item in data:
        logger.debug(f"Поступил запрос: {item=}")
        brand = item.get('brand', 'No brand found')
        article = item.get('article', 'No article found')
        logger.debug(f"Выделили: {brand=}, article: {article=}")

        # Если в JSON нет необходимых ключей, то возвращаем ошибку
        if not brand or not article:
            logger.error("Missing brand or article in request")
            continue

        # Фильтруем имеющиеся данные по полученным параметрам
        list_image = wk_csv.filter(brand=brand, article=article, type_filter='image_link')
        logger.debug(f"Получили по запросу из БД: {list_image=}")

        # Если данные есть добавляем их в ответ на запрос
        if list_image:
            for image in list_image:
                # Т.к. в базе может быть несколько вариантов с одним брендом артикулом, то выбираем точное соответствие
                number = image.get('number', '').split("_")
                if article == number[0]:
                    # Добавляем URL без предварительного экранирования
                    response.append({"url": image['url']})

        # Если данных нет, то возвращаем ошибку
        else:
            logger.info(f"No images found for brand: {brand}, article: {article}")
            abort(404, description="Images not found")

    # Если ответ не сформирован, то возвращаем ошибку
    if not response:
        abort(404, description="No matching images found for any items")

    # Сериализуем в JSON вручную, экранируя символы "/"
    response_json = json.dumps(response).replace("/", "\\/")
    return Response(response_json, mimetype='application/json')


@app.route('/form_deal', methods=['GET', 'POST'])
def form_deal():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO Здесь будет описаны действия с данными заполненной формы.
        #  Отправка в телеграм
        # flash('Login requested for user {}'.format(
        #     form.client.data))
        # flash("Что-то пошло не так", "error")
        return redirect('/form_deal')

    return render_template('form_deal.html', form=form)


if __name__ == '__main__':
    app.run()
