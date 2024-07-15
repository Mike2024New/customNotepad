# import sys
# from PyQt5 import uic
from datetime import datetime

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QListWidget, QLineEdit, QAbstractItemView, QDateTimeEdit, \
    QPushButton, QWidget, QLabel  # QWidget, QApplication,


class ErrorHandler:
    """МЕНЕДЖЕР КОНТЕКСТА - ОБРАБАТЫВАЕТ ОШИБКИ"""

    def __init__(self, blocking: bool, msg="") -> None:
        """
        :param blocking: установка флага -> если True то код продолжится после того как сработало исключение,
        но исключение выведется на консоль (или запишется в журнал)
        если false то сработает reise error и программа будет остановлена
        :param msg: дополнительное сообщение к исключению
        """
        self.blocking = blocking
        self.msg = msg

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"{self.msg}\t - ERROR: {exc_val}")
            return self.blocking
        return True


class ListWidgetBase:
    """Универсальный класс для работы с элементами listWidget (также взаимодействует с listView)"""

    @staticmethod
    def list_widget_set_multiselect_mode(list_widget: QListWidget):
        """
        Сделать возможность выбирать несколько строк в listWidget
        :param list_widget: ссылка на listWidget
        :return:
        """
        list_widget.setSelectionMode(QAbstractItemView.MultiSelection)

    @classmethod
    def list_widget_fill_values_test(cls, list_widget: QListWidget, row_count: int = 10):
        """
        Заполнение ListWidget тестовыми значениями
        :param list_widget: ссылка на list_widget
        :param row_count: количество строк
        :return:
        """
        try:
            for i in range(row_count):
                cls.list_widget_add_row(list_widget, f"test_{i}")
        except Exception as err:
            raise err

    @staticmethod
    def list_widget_add_rows_many(widget: QListWidget, values_list, not_empty_string=True):
        for val in values_list:
            ListWidgetBase.list_widget_add_row(widget, val, not_empty_string=not_empty_string)

    @staticmethod
    def list_widget_add_row(widget: QListWidget, value, not_empty_string=True):
        """
        Добавление строки в listWidget
        Основные:
            :param widget: ссылка на ListWidget
            :param value:записываемое значение
        Опции:
            :param not_empty_string: не принимать пустые строки
            :return:
        """
        try:
            if not_empty_string and value == "":
                return
            widget.addItem(value)
        except Exception as err:
            raise f"Ошибка записи строки {err}"

    @staticmethod
    def list_widget_read_select_row(list_widget: QListWidget) -> str:
        """
        чтение выделенной строки
        :param list_widget: ссылка на listWidget
        :return: значение текущей строки
        """
        try:
            if len(list_widget.selectedIndexes()):
                all_info = list_widget.selectedIndexes()[0]
                out_data = all_info.data()  # текст в строке
                return out_data
        except Exception as err:
            raise err

    @staticmethod
    def list_widget_read_multiselect_row(list_widget: QListWidget) -> list[str]:
        """
        чтение выделенных строк
        :param list_widget: ссылка на listWidget
        :return: список выделенных строк
        """
        try:
            items = list_widget.selectedItems()
            out_values = []
            for i in range(len(items)):
                out_values.append(str(list_widget.selectedItems()[i].text()))
            return out_values
        except Exception as err:
            raise err

    @staticmethod
    def list_widget_delete_select_row(list_widget: QListWidget):
        """
        Можно расширить добавив диалоговое меню с подверждением на удаление
        Удаление выделенной строки
        :param list_widget:ссылка на listWidget
        :return:
        """
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))

    @staticmethod
    def list_widget_delete_all_rows(list_widget: QListWidget):
        try:
            while list_widget.count():
                list_widget.takeItem(0)
        except Exception as err:
            raise Exception(err)

    @staticmethod
    def list_widget_multiselect_delete_selected(list_widget: QListWidget):
        selection = list_widget.selectedIndexes()
        try:
            if selection:
                for index in selection:
                    list_widget.takeItem(index.row())
        except Exception as err:
            raise Exception(err)

    @staticmethod
    def list_widget_sort_rows(list_widget: QListWidget):
        """Сортировка строк"""


class ListWidgetAdvanced(ListWidgetBase):
    """Комбинированные методы работы с виджетами"""

    @classmethod
    def list_widget_transfer_list_widget(cls, list_widget_1: QListWidget, list_widget_2: QListWidget):
        """Перемещение выделенной строки из list_widget_1 в list_widget_2"""
        try:
            data = cls.list_widget_read_select_row(list_widget_1)
            cls.list_widget_delete_select_row(list_widget_1)
            cls.list_widget_add_row(list_widget_2, data)
        except Exception as err:
            print(err)

    @classmethod
    def line_edit_to_list_widget(cls, list_widget: QListWidget, line_edit: QLineEdit, clear_line_edit=True):
        """
        этот метод применим в тех случаях, когда текст нужно считать из поля и вставить его в listWidget
        :param list_widget: ссылка на ListWidget
        :param line_edit: ссылка на lineEdit
        Опции:
            :param clear_line_edit: очищать виджет LineEdit, после вставки текста
            :return:
        """

        try:
            txt = line_edit.text()  # чтение поля
        except Exception as err:
            raise f"Ошибка чтения строки {err}"
        else:
            cls.list_widget_add_row(list_widget, txt)
            if clear_line_edit:
                line_edit.clear()

    @classmethod
    def list_widget_move_down(cls, list_widget: QListWidget):
        """
        перемещение выделенной строки вниз
        :param list_widget: сслыка на listWidget
        :return:
        """
        try:
            value = cls.list_widget_read_select_row(list_widget)
            if len(list_widget.selectedIndexes()):
                row_index = list_widget.selectedIndexes()[0].row()
                list_widget.takeItem(row_index)
                list_widget.insertItem(row_index + 1, value)
                list_widget.setCurrentRow(row_index + 1)
        except Exception as err:
            raise err

    @classmethod
    def list_widget_move_up(cls, list_widget: QListWidget):
        """
        перемещение выделенной строки вверх
        :param list_widget: ссылка на listWidget
        :return:
        """
        try:
            value = cls.list_widget_read_select_row(list_widget)
            if len(list_widget.selectedIndexes()):
                row_index = list_widget.selectedIndexes()[0].row()
                list_widget.takeItem(row_index)
                list_widget.insertItem(row_index - 1, value)
                list_widget.setCurrentRow(row_index - 1)
        except Exception as err:
            raise err


class DateTimeEditBase:
    """класс для работы с DateTimeEdit"""

    @staticmethod
    def get_date_time_edit(widget: QDateTimeEdit):
        """работа с dateTimeEdit"""
        try:
            result = [
                widget.date().year(),
                widget.date().month(),
                widget.date().day(),
                widget.time().hour(),
                widget.time().minute()
            ]
            return datetime(*result)
        except Exception as err:
            raise Exception(err)

    @staticmethod
    def set_date_time_edit(widget: QDateTimeEdit, value: datetime):
        """установка времени в date_time_edit для установки даты в ручную"""
        try:
            date = QDateTime(value.year, value.month, value.day, value.hour,
                             value.minute)  # QDateTime - аналогичен Datetime
            widget.setDate(date.date())  # установка даты
            widget.setTime(date.time())  # установка времени
        except Exception as err:
            print(err)


class EditWidgets:
    def __init__(self):
        self.style = None

    @staticmethod
    def window(widget: QWidget, txt: str, style_css=None):
        """Редактирование главного окна"""
        if txt:
            widget.setWindowTitle(txt)
        if style_css:
            widget.setStyleSheet(style_css)

    @staticmethod
    def btn(widget: QPushButton, txt=None, func=None, style_css=None):
        if txt:
            widget.setText(txt)
        if func:
            # Строка ниже (widget: QWidget = widget) колхозное решение подсветки ошибки в connect, дело в том, что
            # при уровне явного объекта QPushButton метод connect не виден средой pycharm и connect подсвечивается
            # Cannot find reference 'connect' in 'pyqtSignal | pyqtSignal | function'
            widget: QWidget = widget  # можно удалить (ничего не произойдёт кроме подсветки connect)
            widget.clicked.connect(func)
        if style_css:
            widget.setStyleSheet(style_css)  # настройки стилей css

    @staticmethod
    def label(widget: QLabel, txt=None, style_css=None):
        """Редактирование QLabel"""
        if txt:
            widget.setText(txt)
        if style_css:
            widget.setStyleSheet(style_css)


class Windows:
    @staticmethod
    def manager_window_main_question(widget, title: str, func: callable, text: str, style_css: tuple = None):
        """
        Диалоговое окно -> вопрос на который нужно ответить да/нет
        :param text: текст самого вопроса
        :param style_css: (0 window,1 label, 2 btn)
        :param widget: само окно -> виджет на котором есть один label и две кнопки
        :param title: заголовок окна
        :param func: функция которая выполнится если нажать да
        :return:
        """
        new_widget = widget
        widget.label.setText(text)
        if style_css:
            # если стили установлены
            EditWidgets.label(widget, style_css=style_css[1])
            EditWidgets.window(widget, txt=title, style_css=style_css[0])
            EditWidgets.btn(widget.btnYes, func=lambda: func(), style_css=style_css[-1])
            EditWidgets.btn(widget.btnNo, func=lambda: widget.close(), style_css=style_css[-1])
        else:
            EditWidgets.btn(widget.btnYes, func=lambda: func())
            EditWidgets.btn(widget.btnNo, func=lambda: widget.close())
        widget.show()


class WidgetAdapter:
    """класс-посредник который хранит ссылки на все классы виджеты"""

    def __init__(self):
        self.listWidget = ListWidgetAdvanced()
        self.dateTimeEdit = DateTimeEditBase()
        self.editWidget = EditWidgets()
        self.window = Windows()
