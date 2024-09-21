from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, validators
from wtforms.validators import DataRequired
from config import CAR_MODEL, CAR_COLOR, YEAR_PROD


class LoginForm(FlaskForm):
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
        choices=CAR_MODEL,
        validators=[
            DataRequired(message="Это обязательный вопрос."),
            validators.Regexp(r'[^Выбрать]+', message='Это обязательный вопрос.')
        ]
    )
    car_color = SelectField(
        "Цвет авто",
        choices=CAR_COLOR,
        validators=[
            DataRequired(message="Это обязательный вопрос."),
            validators.Regexp(r'[^Выбрать]+', message='Это обязательный вопрос.')
        ]
    )
    year_prod = SelectField(
        "Год выпуска",
        choices=YEAR_PROD,
        validators=[
            DataRequired(message="Это обязательный вопрос."),
            validators.Regexp(r'[^Выбрать]+', message='Это обязательный вопрос.')
        ]
    )
    profit_car_body = StringField(
        "Прибыль с кузова авто",
        validators=[DataRequired(message="Это обязательный вопрос.")],
        render_kw={"placeholder": "Мой ответ"},
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




