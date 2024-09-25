import csv
from loguru import logger


class ReadWriteCSV:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_csv(self):
        """
        Считываем csv файл
        :return: list[dict]
        """
        try:
            with open(self.file_name, encoding='utf-8') as r_file:
                # Создаем объект DictReader, указываем символ-разделитель ","
                return [row for row in csv.DictReader(r_file, delimiter=",")]
        except BaseException as be:
            logger.error(be)
            return []

    def add_to_csv(self, data: list[dict], mode="a") -> bool:
        """
        Записываем данные в файл
        :param mode: режим записи в файл
        :type data: object
        :return:
        """
        if not data:
            return False
        try:
            with open(self.file_name, mode=mode, encoding='utf-8', newline='') as w_file:
                names = data[0].keys()
                file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\r", fieldnames=names)
                if w_file.tell() == 0:
                    file_writer.writeheader()
                for row in data:
                    file_writer.writerow(row)
                return True
        except BaseException as be:
            logger.error(be)
            return False


class WorkCSV:
    def __init__(self, file_name):
        self.csv_rw = ReadWriteCSV(file_name)
        self._data = self.csv_rw.read_csv()  # Загружаем данные из файла
        self._new_data = []

    def filter(self, **kwargs):
        """
        Фильтруем данные из файла csv согласно заданных параметров
        """
        if kwargs['type_filter'] == 'image_link':
            return list(filter(
                lambda v:
                v["brand"].lower() == kwargs['brand'].lower()
                and kwargs['article'].lower() in v["number"].lower(), self._data
            ))

        else:
            return []

    def add_to_data(self, **kwargs):
        """Добавляем данные по позиции в список"""
        if kwargs['type_data'] == 'image_link':
            self._new_data += [{
                'brand': kwargs['brand'],
                'number': kwargs['number'],
                'url': kwargs['url'],
            }]

    def add_data_file(self, mode="w"):
        """
        Сохраняем все накопленные данные в файл для хранения
        """
        self.csv_rw.add_to_csv(self._new_data, mode)
