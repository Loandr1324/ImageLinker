import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from config import TOKEN_BOT, CHAT_ID
from loguru import logger

TOKEN = TOKEN_BOT
CHAT_ID = CHAT_ID
telegramBot = telepot.Bot(token=TOKEN_BOT)


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
    data['profit'] = profit_calculation(data)
    text = generate_text_for_deal(data)
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
    :return: bool - результат отправки
    """
    try:
        telegramBot.sendMessage(CHAT_ID, message, parse_mode="HTML", reply_markup=keyboard)
        return True
    except ConnectionError as ce:
        logger.error('Отправка уведомления в телеграм была неудачна. Описание ошибки:')
        logger.error(ce)
        return False


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