import inspect
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from html_editor import html_insert_tag
from customWidgets import ErrorHandler


class UserForm(QWidget):
    """главное окно приложения, остальные классы подключаются как модули"""

    # noinspection PyUnresolvedReferences
    def __init__(self) -> None:
        super().__init__()
        self.main_window = uic.loadUi('user_forms/notepad3.ui')  # загрузка окна
        self.html_text = self.get_html_edit_text()
        self.main_window.test_btn.clicked.connect(lambda: print(self.get_html_edit_text()))
        self.main_window.test2_btn.clicked.connect(lambda: print(self.get_text_edit_text()))
        self.main_window.test3_btn.clicked.connect(lambda: print(self.get_selected_word()))
        self.main_window.test4_btn.clicked.connect(lambda: self.test_4())
        # флаги для клавиш форматирования Ж К Ч
        self.is_cursive = False  # флаг курсива
        self.is_bold = False  # флаг ожирения текста
        self.is_underline = False  # флаг подчеркивания текста
        self.main_window.btn_bold.clicked.connect(lambda: self.toggle_buttons(command="bold"))
        self.main_window.btn_cursive.clicked.connect(lambda: self.toggle_buttons(command="cursive"))
        self.main_window.btn_underline.clicked.connect(lambda: self.toggle_buttons(command="underline"))
        self.main_window.show()

    def toggle_buttons(self, command: str):
        # ==================================
        if command == "bold":
            self.is_bold = not self.is_bold
            if self.is_bold:
                self.main_window.btn_bold.setStyleSheet("background-color: red;")
            else:
                self.main_window.btn_bold.setStyleSheet("background-color: none;")
        # ==================================
        if command == "cursive":
            self.is_cursive = not self.is_cursive
            if self.is_cursive:
                self.main_window.btn_cursive.setStyleSheet("background-color: red;")
            else:
                self.main_window.btn_cursive.setStyleSheet("background-color: none;")
        # ==================================
        if command == "underline":
            self.is_underline = not self.is_underline
            if self.is_underline:
                self.main_window.btn_underline.setStyleSheet("background-color: red;")
            else:
                self.main_window.btn_underline.setStyleSheet("background-color: none;")

    def test_4(self):
        """временная тестовая функция, которая форматирует текст"""
        # \u2029 - это перенос строки (нужно обработать ситуацию если выделены два параграфа)
        res = self.get_selected_word()
        text = self.get_text_edit_text()
        print(res)
        start_text = res[0]  # стартовая позиция выделенного слова
        row_text = text[:start_text].count("\n")  # строка в которой выделено слово (она же номер тега p)
        start_text = start_text - len("\n".join(text.split("\n")[:row_text])) - 1  # положение слова в строке
        end_text = start_text + (res[1] - res[0])  # финишная позиция выделенного слова
        print(f"start={start_text} end={end_text} row={row_text}")
        with ErrorHandler(blocking=True, msg=f"Ошибка{inspect.currentframe()}"):
            html = self.get_html_edit_text()
            if text:
                print(start_text, end_text)
                result = html_insert_tag(html, num_par=row_text, start=start_text, end=end_text,
                                         bold=self.is_bold, italic=self.is_cursive, underline=self.is_underline,
                                         color="red")  # форматирование
                self.set_text_in_editor(result)

    def set_text_in_editor(self, new_html: str):
        self.main_window.textEdit.setHtml(new_html)

    def get_selected_word(self):
        cursor = self.main_window.textEdit.textCursor()
        if cursor.hasSelection():  # если есть выделение курсора
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            return start, end
        return None, None

    # def get_selected_word(self):
    #     """Получение выделенного слова и его позиции в HTML-коде"""
    #     cursor = self.main_window.textEdit.textCursor()
    #     if cursor.hasSelection():  # если есть выделение курсора
    #         selected_text = cursor.selectedText()
    #         cursor.setPosition(cursor.selectionStart())
    #         word_start = cursor.blockNumber(), cursor.columnNumber()
    #         cursor.setPosition(cursor.selectionEnd())
    #         word_end = cursor.blockNumber(), cursor.columnNumber()
    #         return selected_text, word_start, word_end
    #     return None, None, None

    def get_html_edit_text(self) -> str:
        """возвращает html текст QEditText"""
        return self.main_window.textEdit.toHtml()

    def get_text_edit_text(self) -> str:
        """возвращает простой текст из QTextEdit"""
        return self.main_window.textEdit.toPlainText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_app = UserForm()
    sys.exit(app.exec_())
