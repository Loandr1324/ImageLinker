import asyncio
from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN_BOT, CHAT_ID

TOKEN = TOKEN_BOT
CHATID = CHAT_ID
bot = Bot(token=TOKEN_BOT)
# telegramBot = telepot.Bot(TOKEN)


def create_message(data: dict) -> (str, InlineKeyboardMarkup):
    """
    Генерирует текст сообщения
    :param data: словарь с ключами
    Пример:
    {
        'manager': 'тестМ',
        'client': 'тестК',
        'car_model': 'CS55PLUS',
        'car_color': 'Светло-серый',
        'year_prod': '2025',
        'profit_car_body': 1,
        'profit_add_equip': 2,
        'profit_credit': 3,
        'comp_suppl': 4,
        'trade_in': 'Y',
        'credit': 'Y',
        'kasko': 'Y',
        'date_issue': 'сегодня',
    }
    :return: tuple(
        строка с текстом сообщения и добавленной инлайн клавиатурой,
        экземпляр класса InlineKeyboardMarkup с инлайн клавиатурой
    """
    profit_car_body = data.get('profit_car_body')
    profit_add_equip = data.get('profit_add_equip')
    profit_credit = data.get('profit_credit')
    comp_suppl = data.get('comp_suppl')
    profit = int(profit_car_body) + int(profit_add_equip) + int(profit_credit) + int(comp_suppl)
    # TODO Исправить ссылку на менеджера
    # text = f"""🟡 @Monareich, Просьба
    text = f"""🟡 Monareich, Просьба
    согласовать:
    Менеджер: {data.get('manager')}
    {data.get('client')}
    {data.get('car_model')}
    Цвет: {data.get('car_color')}
    Год: {data.get('year_prod')}
    Ж: {profit_car_body}
    О: {profit_add_equip}
    К: {profit_credit}
    Компенсация: {comp_suppl}
    Трейд-ин: {data.get('trade_in')}
    Кредит: {data.get('credit')}
    КАСКО: {data.get('kasko')}
    Итого = {profit}
    Выдача: {data.get('date_issue')}
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Согласовать", callback_data=f"approve"),
         InlineKeyboardButton(text="🔴 Отклонить", callback_data=f"reject")],
    ])
    return text, keyboard


def send_message(message: str, keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> bool:
    """
    Отправка сообщения в чат телеграм
    :param message: сообщение
    :param keyboard: экземпляр класса клавиатуры для телеграм
    :return:
    """
    try:
        asyncio.run(bot.send_message(CHATID, message, parse_mode="HTML", reply_markup=keyboard))
        return True
    except ConnectionError as ce:
        print('Отправка уведомления в телеграм была неудачна. Описание ошибки:')
        print(ce)
        return False
