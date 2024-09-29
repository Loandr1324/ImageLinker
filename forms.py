from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, validators
from wtforms.validators import DataRequired
from app.db_work import DatabaseConnector
from config import AUTH_mySQL
from loguru import logger


def get_field_value() -> (list, list, list):
    """
    Формируем значение полей формы
    :return:
    """
    # Формируем значения полей из БД
    car_model_value, car_color_value, years_prod = [], [], []
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


class LoginForm(FlaskForm):
    # Получаем значения полей выбора из БД
    car_model_value, car_color_value, year_prod_value = get_field_value()
    manager = StringField(
        "Менеджер",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"}

    )
    client = StringField(
        "ФИО клиента",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"},
    )
    car_model = SelectField(
        "Модель авто",
        choices=car_model_value,
        validators=[
            DataRequired(message="Это обязательный вопрос."),
            validators.Regexp(r'[^Выбрать]+', message='Это обязательный вопрос.')
        ]
    )
    car_color = SelectField(
        "Цвет авто",
        choices=car_color_value,
        validators=[
            DataRequired(message="Это обязательный вопрос."),
            validators.Regexp(r'[^Выбрать]+', message='Это обязательный вопрос.')
        ]
    )
    year_prod = SelectField(
        "Год выпуска",
        choices=year_prod_value,
        validators=[
            DataRequired(message="Это обязательный вопрос."),
            validators.Regexp(r'[^Выбрать]+', message='Это обязательный вопрос.')
        ]
    )
    profit_car_body = StringField(
        "Прибыль с кузова авто",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"}
    )
    profit_add_equip = StringField(
        "Прибыль с доп оборудования",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"}
    )
    profit_credit = StringField(
        "Прибыль от кредита",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"}
    )
    comp_suppl = StringField(
        "Компенсация от поставщика",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"}
    )
    trade_in = RadioField(
        "Трейд ин",
        choices=['Да', 'Нет'],
        validators=[DataRequired(message="Это обязательный вопрос.")]
    )
    credit = RadioField(
        "Кредит", choices=['Да', 'Нет'], validators=[DataRequired(message="Это обязательный вопрос.")]
    )
    kasko = RadioField(
        "КАСКО", choices=['Да', 'Нет'], validators=[DataRequired(message="Это обязательный вопрос.")]
    )
    date_issue = StringField(
        "Дата выдачи",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"}
    )

    submit = SubmitField('Отправить на согласование')
    cleare = SubmitField('Очистить форму')


if __name__ == "__main__":
    # get_field_value()
    pass
