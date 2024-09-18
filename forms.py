from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired
from config import CAR_MODEL, CAR_COLOR, YEAR_PROD


class LoginForm(FlaskForm):
    manager = StringField("Менеджер", validators=[DataRequired(message="Заполните поле")])
    client = StringField("ФИО клиента", validators=[DataRequired(message="Заполните поле")])
    car_model = SelectField("Модель авто", choices=CAR_MODEL, validators=[DataRequired(message="Заполните поле")])
    car_color = SelectField("Цвет авто", choices=CAR_COLOR, validators=[DataRequired(message="Заполните поле")])
    year_prod = SelectField("Год выпуска", choices=YEAR_PROD, validators=[DataRequired(message="Заполните поле")])
    profit_car_body = IntegerField("Прибыль с кузова авто", validators=[DataRequired(message="Заполните поле")])
    profit_add_equip = IntegerField("Прибыль с доп оборудования", validators=[DataRequired(message="Заполните поле")])
    profit_credit = IntegerField("Прибыль от кредита", validators=[DataRequired(message="Заполните поле")])
    comp_suppl = IntegerField("Компенсация от поставщика", validators=[DataRequired(message="Заполните поле")])
    trade_in = RadioField("Трейд ин", choices=['Да', 'Нет'], validators=[DataRequired(message="Заполните поле")])
    credit = RadioField("Кредит", choices=['Да', 'Нет'], validators=[DataRequired(message="Заполните поле")])
    kasko = RadioField("КАСКО", choices=['Да', 'Нет'], validators=[DataRequired(message="Заполните поле")])

    date_issue = StringField("Дата выдачи", validators=[DataRequired(message="Заполните поле")])

    submit = SubmitField('Отправить на согласование')
