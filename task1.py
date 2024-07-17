"""
-----------------------------------------------------------------------------------------------------------
В этом блоке кода реализовано изменение цвета заданных пользователем слов, при этом пользователь сам может
указывать нужное слово и цвет выделения этого слова
-----------------------------------------------------------------------------------------------------------
добавление пунктов меню вверху, можно посмотреть здесь: https://www.youtube.com/watch?v=4Xkr3Dqv384
"""
# import os
import os
import sys
import inspect
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QFont, QKeySequence, QBrush
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QColorDialog, QInputDialog, QAction, QShortcut
from customWidgets import ListWidgetAdvanced  # это самописный адаптер для работы с виджетами (в данном случае listWidg)
from customWidgets import ErrorHandler
from JsonManager import JsonManager

searches_frases = {"123": (255, 0, 0), "test": (0, 128, 0)}  # таблица ключевых слов (потом уберу в json)
json_manager = JsonManager("app_data.json")


class KeyWords(QWidget):
    """
    класс расширение к классу UserForm
    этот класс отвечает за окно менеджера ключевых слов, в нём добавляются новые слова и цвет выделения для них"""

    def __init__(self):
        super().__init__()
        self.test()
        self.LW = ListWidgetAdvanced()  # адаптер для работы с QListWiget
        self.window_keys_words = None  # окно менеджера слов, инициализируется каждый раз при вызове init

    @staticmethod
    def test():
        """создание раздела данных модуля KeyWords в json"""
        data = json_manager.read()
        if "keywords" not in data:
            data["keywords"] = {}
            json_manager.rec(data)

    def window_key_words_init(self) -> None:
        """инициализация окна менеджера добавленных ключевых слов"""
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            self.window_keys_words = uic.loadUi('user_forms/key_words.ui')  # окно с ключевыми словами
            self.window_keys_words.btn_new_words.clicked.connect(lambda: self.window_key_words_edit())  # добавить слово
            self.window_keys_words.btn_del_words.clicked.connect(lambda: self.window_key_words_delete())
            self.window_key_words_show_words()
            self.window_keys_words.show()

    def window_key_words_edit(self) -> None:
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            self.add_key_word()  # добавление нового слова (или обновление старого)
            self.window_key_words_show_words()  # отобразить ключевые слова после добавления нового слова

    def window_key_words_delete(self) -> None:
        """удаление ключевого слова с параметром цвета из search_frases"""
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            words = self.LW.list_widget_read_select_row(list_widget=self.window_keys_words.listWidget)  # получ слова
            if words:
                searches_frases.pop(words.split(" ")[0])
                self.LW.list_widget_delete_select_row(list_widget=self.window_keys_words.listWidget)

    def window_key_words_show_words(self) -> None:
        """отображение ключевых слов на экране (обновление listwidget)"""
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            self.LW.list_widget_delete_all_rows(self.window_keys_words.listWidget)  # удаление всех строк из listWidget
            test_list = [f"{key} : {searches_frases[key]}" for key in searches_frases]  # загрузить все ключ слова
            self.LW.list_widget_add_rows_many(self.window_keys_words.listWidget, values_list=test_list)  # вывести

    def add_key_word(self) -> None:
        """
        Создание нового ключевого слова (редактирование уже существующего), сперва откроется окно которое предложит
        ввести слово, если слово введено, то следом за ним появится окно выбора цвета для этого слова, а за тем
        все слова в тексте соответствующие заданному критерию будут изменены.
        Чуть позже добавленные слова будут сохраняться в json файл, чтобы они сохранялись и после перезапуска программы
        :return:None
        """
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            search_frase, ok = QInputDialog.getText(self, "Добавить слово", "Введите ключевое слово:")
            if ok and search_frase:
                color_dialog = QColorDialog(self)  # окно выбора цвета
                if color_dialog.exec_():
                    print("color exit")
                    selected_color = color_dialog.selectedColor()  # считать выбранный цвет
                    rgb = (selected_color.red(), selected_color.green(), selected_color.blue())  # извлечь rgb
                    searches_frases[search_frase] = rgb  # добавить новую пару значение цвет в коллекцию ключ слов
                    json_manager.add_new_edit_key_value(key=search_frase, value=rgb)
                    self.window_key_words_show_words()  # отобразить ключевые слова после добавления нового слова
                    # self.changed_text()  # Обновляем выделение текста (чтобы изменения сразу же вступили в силу)

    @staticmethod
    def text_format_key_word_color(text_edit: QTextEdit) -> None:
        """
        Изменение цвета текста ключевых слов которые есть в коллекции self.searches_frases, в соответствии с
        цветами заданными пользователем
        :return: None
        """
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            text = text_edit.toPlainText()
            extra_selections = []

            # Ищем все вхождения слова "test" в тексте
            for search_frase in searches_frases:
                format_highlight = QTextCharFormat()
                format_highlight.setForeground(QColor(*searches_frases[search_frase]))  # изменение цвета самого текста
                start = 0
                while True:
                    start = text.find(search_frase, start)
                    if start == -1:
                        break
                    if (start == 0 or text[start - 1].isspace()  # проверка что пробел есть вначале
                            and (start + len(search_frase) >= len(text)  # проверка является ли слово последним в тексте
                                 or text[
                                     start + len(search_frase)].isspace())):  # проверка есть ли пробел после иск слова
                        selection = QTextEdit.ExtraSelection()
                        selection.format = format_highlight
                        selection.cursor = text_edit.textCursor()
                        selection.cursor.setPosition(start)
                        selection.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(search_frase))
                        extra_selections.append(selection)
                    start += len(search_frase)

                    # Применяем выделения к QTextEdit
                    text_edit.setExtraSelections(extra_selections)


class UserForm(QWidget):
    """главное окно приложения, остальные классы подключаются как модули"""

    # noinspection PyUnresolvedReferences
    def __init__(self) -> None:
        super().__init__()
        self.main_window = uic.loadUi('user_forms/notepad3.ui')  # загрузка окна
        self.main_window.textEdit.textChanged.connect(self.changed_text)  # реакция на любое изменение текста в поле
        self.checker_json()  # проверка есть ли json файл приложения, если нет то создать
        self.assigning_hotkeys()  # подключение комбинаций горячих клавиш
        self.is_italic = False  # флаг курсива
        self.is_bold = False  # флаг ожирения текста
        self.is_underline = False  # флаг подчеркивания текста
        self.main_window.btn_bold.clicked.connect(lambda: self.toggle_buttons(command="bold"))
        self.main_window.btn_cursive.clicked.connect(lambda: self.toggle_buttons(command="italic"))
        self.main_window.btn_underline.clicked.connect(lambda: self.toggle_buttons(command="underline"))
        self.main_window.test_btn.clicked.connect(lambda: self.get_html())
        self.main_window.test2_btn.clicked.connect(lambda: self.get_text())
        self.main_window.test3_btn.clicked.connect(lambda: self.set_text_in_editor())
        self.main_window.test4_btn.clicked.connect(lambda: print("заглушка"))
        self.main_window.show()
        self.actions_list = []  # - функции которые будут срабатывать при изменении TextEdit
        self.apply_text_format()
        # ===========================================================
        # Меню бар в верху (встроенные пункты меню, по умолчанию)
        menubar = self.main_window.menuBar()  # создание объекта меню
        file_menu = menubar.addMenu('Меню')  # добавление вкладки в верхнее меню
        # ===========================================================
        """ПОДКЛЮЧАЕМЫЕ МОДУЛИ - к модулям есть требование, все их методы должны быть обложены try/except, чтобы
        непредвиденные ошибки не привели к вылету основного приложения"""

        # noinspection PyUnresolvedReferences

        def test():
            """
            подключение KeyWords - выделения цветом ключевых слов (добавление ключевых слов)
            временно сделан через функцию, потом этот модуль переместить в инициализатор класса KeyWords(), а в этом
            классе сделать лоадер для подключаемых расширений
            :return:
            """
            self.window_key_words = KeyWords()  # менеджер подсветки ключевых слов (как в редакторах кода)
            self.window_keys_words = None  # окно с ключевыми словами (загружается только внутри своей функции)
            self.actions_list.append(lambda: KeyWords.text_format_key_word_color(text_edit=self.main_window.textEdit))

            btn_action = QAction('Ключевые слова', self.main_window)  # создание кнопки для меню
            btn_action.triggered.connect(lambda: self.window_key_words.window_key_words_init())
            file_menu.addAction(btn_action)  # размещение кнопки на вкладке

        test()  # подключение менеджера ключевых слов

        # ===========================================================
        """ДОБАВЛЕНИЕ КНОПКИ ВЫХОД (РАЗМЕЩЕНО ЗДЕСЬ, ПОСЛЕ КНОПОК ПОДКЛЮЧАЕМЫХ МОДУЛЕЙ)"""
        new_action = QAction('Выход', self.main_window)  # создание кнопки для меню
        new_action.triggered.connect(lambda: self.main_window.close())  # подключение сигнала к слоту (назнач функцию)
        file_menu.addAction(new_action)  # размещение кнопки на вкладке

    def get_html(self):
        html = self.main_window.textEdit.toHtml()
        # print(html)
        return html

    def get_text(self):
        # textEdit = QTextEdit()
        # textEdit.toPlainText()
        text = self.main_window.textEdit.toPlainText()
        print(text)

    def set_text_in_editor(self):
        # форматирование нужно делать через html, при этом меняя (удаляя старые теги)
        with ErrorHandler(blocking=True, msg=f"Ошибка расширения {inspect.currentframe()}"):
            html: str = self.get_html()
            print(html)
            # нужно заменить исходный test
            html = html.replace("for", """<span style=" color:#0000ff;">for</span>""")
            print(html)
            self.main_window.textEdit.setHtml(html)

    @staticmethod
    def checker_json():
        data = {}
        if not os.path.exists(json_manager.file):
            json_manager.rec(data)

    def changed_text(self):
        """
        Метод срабатывает на любое изменение текста в TextEdit и запускает команды из self.actions_list
        :return: None
        """
        with ErrorHandler(blocking=True, msg=f"Ошибка расширения {inspect.currentframe()}"):
            [func() for func in self.actions_list]

    # noinspection PyUnresolvedReferences
    def assigning_hotkeys(self) -> None:
        """привязка горячих клавиш к функциям"""
        # при нажатии на ctrl+b будет выполняться функция сделать текст жирным
        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_B), self.main_window).activated.connect(
            lambda: self.toggle_buttons(command="bold"))  # сделать текст жирным / или наоборот

        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_I), self.main_window).activated.connect(
            lambda: self.toggle_buttons(command="italic"))  # сделать текст наклонным

        QShortcut(QKeySequence(Qt.CTRL + Qt.Key_U), self.main_window).activated.connect(
            lambda: self.toggle_buttons(command="underline"))  # сделать текст наклонным

    def toggle_buttons(self, command: str) -> None:
        """
        toggle - кнопки
        :param command: italic; bold; underline
        :return:
        """
        """подключаемые модули"""
        # ======== КУРСИВ ТЕКСТА ====================
        if command == "italic":
            self.is_italic = not self.is_italic
            if self.is_italic:
                self.main_window.btn_cursive.setStyleSheet("background-color: red;")
            else:
                self.main_window.btn_cursive.setStyleSheet("background-color: none;")

        # ======= ОЖИРЕНИЕ ТЕКСТА ===================
        elif command == "bold":
            self.is_bold = not self.is_bold
            if self.is_bold:
                self.main_window.btn_bold.setStyleSheet("background-color: red;")
            else:
                self.main_window.btn_bold.setStyleSheet("background-color: none;")

        # ======= ПОДЧЕРКИВАНИЕ ТЕКСТА ==============
        elif command == "underline":
            self.is_underline = not self.is_underline
            if self.is_underline:
                self.main_window.btn_underline.setStyleSheet("background-color: red;")
            else:
                self.main_window.btn_underline.setStyleSheet("background-color: none;")

        """действия после определения toggle button"""
        self.apply_text_format()  # применение форматирования
        cursor = self.main_window.textEdit.textCursor()  # Сохраняем текущий курсор
        self.main_window.textEdit.setTextCursor(cursor)  # Восстанавливаем курсор на прежнее место
        self.main_window.textEdit.setFocus()  # Возвращаем фокус на текстовое поле

    def apply_text_format(self):
        """применение формата к тексту: жирный, кривой, подчёркнутый"""
        font_size = 12
        with ErrorHandler(blocking=True, msg=f"Ошибка {inspect.currentframe()}"):
            print("apply_format")
            cursor = self.main_window.textEdit.textCursor()
            char_format = QTextCharFormat()
            font = char_format.font()
            font.setFamily(self.main_window.font().family())
            font.setPointSize(font_size)  # предустановленный шрифт (позже будет скачиваться из настроек)
            font.setStyle(font.StyleItalic if self.is_italic else font.StyleNormal)  # наклонный текст italic
            font.setBold(self.is_bold)  # жирный текст bold
            char_format.setFont(font)  # применение стилей к тексту (важно чтобы эта строка была перед underline)
            char_format.setFontUnderline(self.is_underline)  # подчеркивание текста
            cursor.setCharFormat(char_format)
            self.main_window.textEdit.setTextCursor(cursor)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_app = UserForm()
    sys.exit(app.exec_())
