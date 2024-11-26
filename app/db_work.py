import mysql.connector
from mysql.connector import Error
from loguru import logger


class DatabaseConnector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """Подключаемся к базе данных"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                logger.info("Успешно подключились к базе данных")
        except Error as e:
            logger.error(f"Ошибка при подключении к MySQL: {e}")

    def insert_row(self, table_name, data_deal: dict) -> None or int:
        """
        Записываем строку в базу данных
        :param table_name: Имя таблицы в базе данных
        :param data_deal: словарь с данными для записи
        :return:
        """
        columns_names = [
            "manager", "client", "car_model", "car_color", "year_prod", "profit_car_body", "profit_add_equip",
            "profit_credit", "comp_suppl", "trade_in", "credit", "kasko", "profit", "date_issue"
        ]
        columns_names_int = ["profit_car_body", "profit_add_equip", "profit_credit", "comp_suppl", "profit"]
        # Задаём статус по умолчанию
        columns_query = 'status,'
        values_query = '"новая", '

        # Дополняем строки наименования столбцов таблицы и их значений
        for item in columns_names:
            # Удаляем кавычки из значений
            data_deal[item] = data_deal[item].replace('"', '')

            # Удаляем разделение разрядов по числовым данным
            if item in columns_names_int:
                data_deal[item] = data_deal[item].replace(' ', '')
            # Добавляем наименование колонки в строку
            columns_query += f' {item},'
            # Добавляем значение соответствующей колонки в строку
            values_query += f' "{data_deal[item]}",'

        # Формируем текст запроса для записи строки в БД
        text_query = f"INSERT INTO {table_name} ({columns_query[:-1]}) VALUES({values_query[:-1]});"

        # Выполняем запись в БД и получаем id записанной строки
        id_row = self.run_query_db(text_query)

        return id_row

    def run_query_db(self, query: str) -> None or int:
        """
        Выполняем запрос с проверкой подключения и обработкой ошибок
        :param query: Строка запроса на языке mySQL
        :return: Результат выполнения запроса
        """
        if self.connection is None or not self.connection.is_connected():
            logger.error("Не подключен к базе данных")
            return None

        cursor = self.connection.cursor(dictionary=True)
        try:
            # Выполняем запрос
            cursor.execute(f"{query}")

            # Получаем ID последней записи
            last_id = cursor.lastrowid

            # Применяем изменения в БД
            self.connection.commit()
            return last_id
        except Error as e:
            logger.error(f"Ошибка при работе с базой данных MySQL: {e}")
            return None
        finally:
            cursor.close()

    def fetch_all_positions(self, table_name: str) -> list[dict] or None:
        """
        Получаем данные из указанной таблицы
        :param table_name: Имя таблицы
        :return: Список словарей с данными из указанной таблицы
        """
        if self.connection is None or not self.connection.is_connected():
            logger.error("Не подключен к базе данных")
            return None

        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            return records
        except Error as e:
            logger.error(f"Ошибка при получении данных из таблицы MySQL: {e}")
            return None
        finally:
            cursor.close()

    def close_connection(self):
        """Закрываем соединение с БД"""
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            logger.info("Соединение MySQL закрыто")


# Пример для тестирования
if __name__ == "__main__":
    data = {}
    from config import AUTH_mySQL

    db_connector = DatabaseConnector(
        host=AUTH_mySQL['host'],
        database=AUTH_mySQL['database'],
        user=AUTH_mySQL['user'],
        password=AUTH_mySQL['password']
    )
    db_connector.connect()
    result_tg = db_connector.insert_row("sa_deal", data)

    db_connector.close_connection()
    logger.debug(f"{result_tg}")
