# Author Loik Andrey mail: loikand@mail.ru
from flask import Flask, request, abort, Response, render_template, flash, redirect
import json
from flask_cors import CORS
from loguru import logger
from config import FILE_NAME_LOG_LINK, FILE_NAME_IMAGE_LINK, SECRET_KEY, AUTH_mySQL
from data.csv_work import WorkCSV
from forms import LoginForm
import app.send_telegram as st
from app.db_work import DatabaseConnector

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

    # logger.debug(f"Поступили параметры: {data=}")

    # Получаем данные из базы данных по существующим ссылкам
    wk_csv = WorkCSV(FILE_NAME_IMAGE_LINK)

    # Формируем ответ на POST запрос из имеющихся данных
    response = []
    for item in data:
        # logger.debug(f"Поступил запрос: {item=}")
        brand = item.get('brand', 'No brand found')
        article = item.get('article', 'No article found')
        # logger.debug(f"Выделили: {brand=}, article: {article=}")

        # Если в JSON нет необходимых ключей, то возвращаем ошибку
        if not brand or not article:
            logger.error("Missing brand or article in request")
            continue

        # Фильтруем имеющиеся данные по полученным параметрам
        list_image = wk_csv.filter(brand=brand, article=article, type_filter='image_link')
        list_image = sorted(list_image, key=lambda x: x['url'])  # сортируем по значению ключа url
        # logger.debug(f"Получили по запросу из БД: {list_image=}")

        # # TODO Удалить после тестов одного изображения для бренда hyundai-kia
        # if brand.lower() == 'hyundai-kia':
        #     list_image = [{
        #         "number": article,
        #         "url": "https://img.smart-a.ru/images/test/01.jpg"
        #     }]

        # Если данные есть добавляем их в ответ на запрос
        if list_image:
            for image in list_image:
                # Т.к. в базе может быть несколько вариантов с одним брендом артикулом, то выбираем точное соответствие
                number = image.get('number', '').split("_")
                if article.lower() == number[0].lower():
                    # Добавляем URL без предварительного экранирования
                    response.append({"url": image['url']})
            logger.info(f"Отправлено изображение для пары brand: {brand}, article: {article}")

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
    # Создаём экземпляр формы с полями
    form = LoginForm()

    # Задаём значение полей из БД
    set_choices_select_field_value(form)

    # Действие при нажатии кнопки "Очистить форму"
    if form.cleare.data:
        return redirect(f'/form_deal?manager={form.manager.data}')

    # Проверка полей при нажатии кнопки "Отправить на согласование" и проверки их на заполнение
    if form.validate_on_submit():
        # Рассчитываем прибыль по сделке
        deal_data = form.data.copy()
        deal_data['profit'] = profit_calculation(form.data)

        # Записываем в БД данные о сделке
        id_row = save_db(deal_data.copy())

        # Отправляем сообщение в телеграм, если запись в БД прошла успешно
        if id_row:
            deal_data['id_row'] = id_row

            # Проверяем запрос на пересогласование
            message_id = request.args.get('message_id')
            chat_id = request.args.get('chat_id')

            # Редактируем предыдущее сообщение, которое отправлено на пересогласование
            if message_id:
                message, keyboard = st.create_message(request.args, "edit")
                result_tg = st.edit_message(message, message_id, chat_id, keyboard)

            # Отправляем сообщение в телеграм с данными из формы
            message, keyboard = st.create_message(deal_data, "send")
            result_tg = st.send_message(message, message_id, chat_id, keyboard)
        else:
            result_tg = False

        # Контролируем результат выполнения
        if id_row and result_tg:
            return redirect(f'/form_deal?manager={form.manager.data}')
            # return redirect(f'https://t.me/chng_sale_deal_bot')
            # return redirect(f'https://t.me/+zLWXBFPLmAw4MTg6')
            # return redirect(f'tg:resolve')
        else:
            flash("Форма не была отправлена в телеграм. Убедитесь, что работает телеграм и отправьте заново.\n"
                  "Если ошибка повторяется, то обратитесь к администратору")

    # Заполняем поля формы полученными параметрами
    set_default_form_values(form, request)

    return render_template('form_deal.html', form=form)


def profit_calculation(data: dict) -> str:
    """
    Рассчитываем прибыль по сделке
    :param data: Словарь с ключами
        {'profit_car_body': str,
        'profit_add_equip': str,
        'profit_credit': str,
        'comp_suppl', str}
    :return: Возвращаем сумму в виде строки разделённую по разрядам. Например: "12 681 682"
    """
    profit_car_body = data.get('profit_car_body').replace(' ', '')
    profit_add_equip = data.get('profit_add_equip').replace(' ', '')
    profit_credit = data.get('profit_credit').replace(' ', '')
    comp_suppl = data.get('comp_suppl').replace(' ', '')
    profit = int(profit_car_body) + int(profit_add_equip) + int(profit_credit) + int(comp_suppl)
    return '{0:,}'.format(profit).replace(',', ' ')


def save_db(data: dict) -> None or int:
    """
    Записываем данные о сделки в базу данных
    :param data:
    :return: результат записи в базу БД
    """
    # Записываем данные по сделке в БД
    db_connector = DatabaseConnector(
        host=AUTH_mySQL['host'],
        database=AUTH_mySQL['database'],
        user=AUTH_mySQL['user'],
        password=AUTH_mySQL['password']
    )
    db_connector.connect()
    result = db_connector.insert_row("sa_deal", data)
    db_connector.close_connection()
    return result


def get_field_value() -> (list, list, list):
    """
    Формируем значение полей формы
    :return:
    """
    # Формируем значения полей из БД
    car_model_value, car_color_value, years_prod = ['Выбрать'], ['Выбрать'], ['Выбрать']
    for item in get_table_from_db():
        car_model_value.append(item['car_model']) if item['car_model'] else None
        car_color_value.append(item['car_color']) if item['car_color'] else None
        years_prod.append(item['years_production'].split('.')[0]) if item['years_production'] else None

    return car_model_value, car_color_value, years_prod


def get_table_from_db() -> list[dict]:
    """
    Получаем данные из таблицы БД со значениями форм полей
    :return: таблица словарей со строками БД
    """
    db_connector = DatabaseConnector(
        host=AUTH_mySQL['host'],
        database=AUTH_mySQL['database'],
        user=AUTH_mySQL['user'],
        password=AUTH_mySQL['password']
    )
    db_connector.connect()
    table_from_db = db_connector.fetch_all_positions("sa_cfg_form_deal")
    db_connector.close_connection()

    return table_from_db


def set_default_form_values(form: LoginForm, req) -> None:
    """
    Предварительно заполняем поля формы
    :param form: Экземпляр класс LoginForm с заданными полями
    :param req: Входящие параметры запроса
    :return:
    """
    for item in req.args:
        req.args[item].replace('%20', ' ')

    # Устанавливаем значения поля менеджера из параметров запроса
    form.manager.data = req.args.get('manager') or form.manager.data
    form.client.data = req.args.get('client') or form.client.data
    form.car_model.data = req.args.get('car_model') or form.car_model.data
    form.car_color.data = req.args.get('car_color') or form.car_color.data
    form.client.data = req.args.get('client') or form.client.data
    form.year_prod.data = req.args.get('year_prod') or form.year_prod.data
    form.profit_car_body.data = req.args.get('profit_car_body') or form.profit_car_body.data
    form.profit_add_equip.data = req.args.get('profit_add_equip') or form.profit_add_equip.data
    form.profit_credit.data = req.args.get('profit_credit') or form.profit_credit.data
    form.comp_suppl.data = req.args.get('comp_suppl') or form.comp_suppl.data
    form.trade_in.data = req.args.get('trade_in') or form.trade_in.data
    form.credit.data = req.args.get('credit') or form.credit.data
    form.kasko.data = req.args.get('kasko') or form.kasko.data
    form.date_issue.data = req.args.get('date_issue') or form.date_issue.data

    # Меняем наименование кнопки при пересогласовании
    if req.args.get('message_id'):
        form.submit.label.text = "Отправить на пересогласование"


def set_choices_select_field_value(form: LoginForm) -> None:
    """
    Задаём списки выбора полей SelectField
    :param form: Экземпляр класс LoginForm с заданными полями
    :return:
    """
    # Получаем значения полей выбора из БД
    car_model_value, car_color_value, year_prod_value = get_field_value()
    form.car_model.choices = car_model_value
    form.car_color.choices = car_color_value
    form.year_prod.choices = year_prod_value


if __name__ == '__main__':
    app.run()
