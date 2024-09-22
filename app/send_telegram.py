import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from config import TOKEN_BOT, CHAT_ID
from loguru import logger

TOKEN = TOKEN_BOT
CHAT_ID = CHAT_ID
telegramBot = telepot.Bot(token=TOKEN_BOT)


def generate_text_for_deal(data: dict) -> str:
    """
    Генерируем текст сообщения по сделке для отправки в телеграмм
    :param data:
    :return: str - строка с текстом сообщения
    """
    # return f"""🟡 @Monareich, Просьба согласовать:  # TODO Исправить ссылку на менеджера
    return f"""🟡 Monareich, Просьба согласовать:
    Менеджер: {data.get('manager')}
    {data.get('client')}
    {data.get('car_model')}
    Цвет: {data.get('car_color')}
    Год: {data.get('year_prod')}
    Ж: {data.get('profit_car_body')}
    О: {data.get('profit_add_equip')}
    К: {data.get('profit_credit')}
    Компенсация: {data.get('comp_suppl')}
    Трейд-ин: {data.get('trade_in')}
    Кредит: {data.get('credit')}
    КАСКО: {data.get('kasko')}
    Итого = {data.get('profit')}
    Выдача: {data.get('date_issue')}
    """


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
    text = generate_text_for_deal(data)
    # Генерируем клавиатуру
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Согласовать", callback_data=f"approve_{data.get('id_row')}"),
         InlineKeyboardButton(text="🔴 Отклонить", callback_data=f"reject_id{data.get('id_row')}")]
    ])
    return text, keyboard


def send_message(message: str, keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> bool:
    """
    Отправка сообщения в чат телеграм
    :param message: сообщение
    :param keyboard: экземпляр класса клавиатуры для телеграм
    :return: bool - результат отправки
    """
    try:
        telegramBot.sendMessage(CHAT_ID, message, parse_mode="HTML", reply_markup=keyboard)
        return True
    except ConnectionError as ce:
        logger.error('Отправка уведомления в телеграм была неудачна. Описание ошибки:')
        logger.error(ce)
        return False



