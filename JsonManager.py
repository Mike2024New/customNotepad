import json
import os


class JsonManager:
    """универсальный класс для работы с json подойдёт и для других проектов"""

    def __init__(self, file: str) -> None:
        """
        :param file: путь к файлу
        """
        self.file = file

    def read(self) -> dict or None:
        """
        Чтение json файла извлечение всех данных
        :return: dict с данными или None если файл отсутствует
        """
        if os.path.exists(self.file):
            with open(self.file, encoding="utf-8") as f:
                data_output = json.load(f)
                return data_output
        return None

    def rec(self, data_in: dict) -> None:
        """

        :param data_in: записываемые данные в виде словаря dict
        :return: None
        """
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(data_in, f, ensure_ascii=False, indent=2)

    def add_new_edit_key_value(self, key, value) -> None:
        """
        добавление новой пары ключ-значение в json файл или редактирование уже существующей
        :param key: ключ
        :param value: значение
        :return: None
        """
        data_in = self.read()
        if data_in:
            data_in[key] = value
            self.rec(data_in=data_in)

    def delete_key_value(self, key) -> None:
        """
        удаление конкретной пары ключ значение
        :param key: ключ
        :return: None
        """
        data_in = self.read()
        if data_in:
            if key in data_in:
                data_in.pop(key)
                self.rec(data_in=data_in)

    def get_key_value(self, key) -> object:
        """
        получение конкретного значения по ключу
        :param key: ключ
        :return: значение
        """
        data_in = self.read()
        if data_in:
            if key in data_in:
                return data_in[key]

    def __str__(self):
        return self.file


if __name__ == '__main__':
    json_manager = JsonManager(file="test.json")
    # json_manager.delete_key_value(key="test3")
    # print(json_manager.get_key_value(key="test2"))
    print(json_manager)
