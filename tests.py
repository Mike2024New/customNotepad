import sys
from PyQt5 import uic
from PyQt5.QtGui import QTextDocument

from PyQt5.QtWidgets import QWidget, QApplication


class UserForm(QWidget):
    """главное окно приложения, остальные классы подключаются как модули"""

    # noinspection PyUnresolvedReferences
    def __init__(self) -> None:
        super().__init__()
        self.html_text = """
                <html>
                    <head>
                        <style>
                            .bold { font-weight: bold; }
                            .italic { font-style: italic; }
                            .underline { text-decoration: underline; }
                            .green { color: green; }
                        </style>
                    </head>
                    <body>
                        <p>Hello, <span class="bold">world</span>!</p>
                    </body>
                </html>
                """
        self.main_window = uic.loadUi('user_forms/notepad3.ui')  # загрузка окна
        self.main_window.test_btn.clicked.connect(lambda: self.apply_formatting(format_type="bold", apply=True))
        self.set_text_in_editor()
        self.main_window.show()

    def set_text_in_editor(self):
        self.main_window.textEdit.setHtml(self.html_text)

    def get_selected_word(self):
        """Получение выделенного слова и его позиции в HTML-коде"""
        cursor = self.main_window.textEdit.textCursor()
        if cursor.hasSelection():  # если есть выделение курсора
            selected_text = cursor.selectedText()
            cursor.setPosition(cursor.selectionStart())
            word_start = cursor.blockNumber(), cursor.columnNumber()
            cursor.setPosition(cursor.selectionEnd())
            word_end = cursor.blockNumber(), cursor.columnNumber()
            return selected_text, word_start, word_end
        return None, None, None

    def apply_formatting(self, format_type, apply):
        selected_text, word_start, word_end = self.get_selected_word()
        if selected_text:
            if format_type == "bold":
                if apply:
                    print(self.html_text)
                    self.html_text = self.html_text[:word_start[1]] + \
                                     f"<span class=\"bold\">{selected_text}</span>" + \
                                     self.html_text[word_end[1]:]
                else:
                    self.html_text = self.html_text[:word_start[1]] + \
                                     selected_text + \
                                     self.html_text[word_end[1]:]
        self.set_text_in_editor()

    def get_formatted_text(self):
        return self.html_text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_app = UserForm()
    sys.exit(app.exec_())
