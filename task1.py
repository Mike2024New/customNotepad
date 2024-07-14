"""
-----------------------------------------------------------------------------------------------------------
В этом блоке кода реализовано изменение цвета заданных пользователем слов, при этом пользователь сам может
указывать нужное слово и цвет выделения этого слова
-----------------------------------------------------------------------------------------------------------
добавление пунктов меню вверху, можно посмотреть здесь: https://www.youtube.com/watch?v=4Xkr3Dqv384
"""
import sys
from PyQt5 import uic
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QColorDialog, QInputDialog


class UserForm(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.main_window = uic.loadUi('user_forms/notepad2.ui')
        self.searches_frases = {"123": (255, 0, 0), "test": (0, 128, 0)}  # таблица ключевых слов (потом уберу в json)
        self.main_window.textEdit.textChanged.connect(self.changed_text)  # реакция на любое изменение текста в поле
        self.main_window.action_tab_replace.triggered.connect(self.add_key_word)
        self.main_window.action_exit.triggered.connect(lambda: self.main_window.close())  # кнопка выход (меню бар)
        self.main_window.show()

    def changed_text(self) -> None:
        """
        Изменение цвета текста ключевых слов которые есть в коллекции self.searches_frases, в соответствии с цветами
        заданными пользователем
        :return: None
        """
        text_edit = self.main_window.textEdit
        text = text_edit.toPlainText()

        extra_selections = []

        # Ищем все вхождения слова "test" в тексте
        for search_frase in self.searches_frases:
            format_highlight = QTextCharFormat()
            format_highlight.setForeground(QColor(*self.searches_frases[search_frase]))  # изменение цвета самого текста
            start = 0
            while True:
                start = text.find(search_frase, start)
                if start == -1:
                    break
                if (start == 0 or text[start - 1].isspace()  # проверка что пробел есть вначале
                        and (start + len(search_frase) >= len(text)  # проверка является ли слово последним в тексте
                             or text[
                                 start + len(search_frase)].isspace())):  # проверка есть ли пробел после искомого слова
                    selection = QTextEdit.ExtraSelection()
                    selection.format = format_highlight
                    selection.cursor = text_edit.textCursor()
                    selection.cursor.setPosition(start)
                    selection.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(search_frase))
                    extra_selections.append(selection)
                start += len(search_frase)

                # Применяем выделения к QTextEdit
                text_edit.setExtraSelections(extra_selections)

    def add_key_word(self) -> None:
        """
        Создание нового ключевого слова (редактирование уже существующего), сперва откроется окно которое предложит
        ввести слово, если слово введено, то следом за ним появится окно выбора цвета для этого слова, а за тем
        все слова в тексте соответствующие заданному критерию будут изменены.
        Чуть позже добавленные слова будут сохраняться в json файл, чтобы они сохранялись и после перезапуска программы
        :return:None
        """
        search_frase, ok = QInputDialog.getText(self, "Добавить слово", "Введите ключевое слово:")
        if ok and search_frase:
            color_dialog = QColorDialog(self)  # окно выбора цвета
            if color_dialog.exec_():
                selected_color = color_dialog.selectedColor()  # считать выбранный цвет
                rgb = (selected_color.red(), selected_color.green(), selected_color.blue())  # извлечь rgb
                self.searches_frases[search_frase] = rgb  # добавить новую пару значение цвет в коллекцию ключ слов
                self.changed_text()  # Обновляем выделение текста (чтобы изменения сразу же вступили в силу)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_app = UserForm()
    sys.exit(app.exec_())
