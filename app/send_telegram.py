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
    return f"""🟡 @Monareich, Просьба согласовать:
    Менеджер: <b>{data.get('manager')}</b>
    Клиент: <b>{data.get('client')}</b>
    А/м: <b>{data.get('car_model')}</b>
    Цвет: <b>{data.get('car_color')}</b>
    Год: <b>{data.get('year_prod')}</b>
    Ж: <b>{data.get('profit_car_body')}</b>
    О: <b>{data.get('profit_add_equip')}</b>
    К: <b>{data.get('profit_credit')}</b>
    Компенсация: <b>{data.get('comp_suppl')}</b>
    Трейд-ин: <b>{data.get('trade_in')}</b>
    Кредит: <b>{data.get('credit')}</b>
    КАСКО: <b>{data.get('kasko')}</b>
    <u>Итого = <b>{data.get('profit')}</b></u>
    Выдача: <b>{data.get('date_issue')}</b>
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
        [InlineKeyboardButton(text="🟢 Согласовать", callback_data=f"approve_id{data.get('id_row')}"),
         InlineKeyboardButton(text="🔴 Отклонить", callback_data=f"reject_id{data.get('id_row')}")]
    ])
    return text, keyboard


def send_message(
        message: str,
        keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup,
        message_id: str | int,
        chat_id: str | int
) -> bool:
    """
    Отправка сообщения в чат телеграм
    :param message: Текст сообщения
    :param keyboard: Инланй или Репли клавиатура
    :param message_id: Идентификатор сообщения в чате
    :param chat_id: Чат в котором находится сообщение
    :return: Результат выполнения
    """
    try:
        chat_id = chat_id or CHAT_ID
        telegramBot.sendMessage(
            chat_id, message, parse_mode="HTML", reply_markup=keyboard, reply_to_message_id=message_id
        )
        return True
    except ConnectionError as ce:
        logger.error('Отправка уведомления в телеграм была неудачна. Описание ошибки:')
        logger.error(ce)
        return False
