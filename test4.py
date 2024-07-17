import re

html_text = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Liberation Mono'; font-size:12pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">test for example</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">proga <span style=" color:#aa0000;">123</span> text</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">exit</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>"""
# print(html_text)
simple_text = """test for example
proga 123 text
exit"""  # из QTextEdit получаем простой текст


def html_insert_tag(html: str, text: str, num_par: int, start: int,
                    end: int, bold=False, italic=False, underline=False, color=None):
    """
    Добавление тега span со стилями форматирования в html коде
    :param num_par: номер параграфа
    :param start: стартовая позиция выделенного текста
    :param end: финишная позиция выделенного текста
    :param html: исходный html код
    :param text: исходный текст из QTextEdit (без html разметки)
    :param bold: сделать ли текст жирным?
    :param italic: сделать ли текст наклонным?
    :param underline: сделать ли текст подчёркнутым?
    :param color: какой цвет будет у текста None или конкретный цвет?
    :return: html код с добавленным форматированием
    """

    # 1. преобразование html
    body_pattern = r'<p[^>]*>.+?</p>'  # извлечение контента из body
    paragraphs = re.findall(body_pattern, html, re.DOTALL)  # извлекаем все теги p (строки)
    html = html.replace("\n".join(paragraphs), "~***~")  # удаляем теги p из html (то есть всю внутрянку)

    # 2. преобразование текста (поиск позиции выделения в конкретной строке)
    search_phrase = "it"
    start_text = text.find(search_phrase)  # стартовая позиция выделенного слова
    row_text = text[:start_text].count("\n")  # строка в которой выделено слово (она же номер тега p)
    start_text = start_text - len("\n".join(text.split("\n")[:row_text])) - 1  # положение слова в строке
    end_text = start_text + len(search_phrase)  # финишная позиция выделенного слова

    # 3. поиск соответствия выделенн позиции в html (в теге p), для оптимиз алгоритма поиск ведется только в 1 строке
    html_start = None  # стартовая позиция выделенного слова в html коде
    html_end = None  # конечная позиция выделенного слова в html коде
    html_position_global = 0  # глобальный счётчик, считает все символы подряд
    html_position_local = 0  # локальный счётчик, считает только те символы которые вне html тегов (то есть текст)
    is_tag = True  # флаг, определяющий где находится цикл, внутри тега или снаружи (в контенте - тексте параграфа)

    for i in paragraphs[row_text]:
        """алгоритм обходит все символы абзаца, если символ находится в теге (is_tag), то обновить только глобальный
        счётчик символов, если символ(i), находится вне тега(в тексте), то обновить и глобальный и локальный счетчики
        таким образом достигается совпадение символов в простом тексте и html документе"""
        if i == "<":  # точка открытия тега
            is_tag = True
        elif i == ">":  # точка закрытия тега
            is_tag = False
        if not is_tag and i != ">" and i != "<":
            """если находится вне тега, то есть в самом контексте (тексте параграфа)"""
            if html_position_local == start_text:
                """если локальная позиция, совпадает с положением в простом тексте"""
                html_start = html_position_global
            elif html_position_local == end_text - 1:
                """если локальная позиция, совпадает с положением в простом тексте"""
                html_end = html_position_global + 1
            html_position_local += 1  # так как мы вне тега, то увеличиваем local на +1
        html_position_global += 1  # каждый символ подряд глобальный счётчик обновляется

    # сборка обновленного html
    left_paragraph = paragraphs[row_text][:html_start]  # часть параграфа до выделенного текста
    right_paragraph = paragraphs[row_text][html_end:]  # часть параграфа после выделенного текста
    replacer_paragraph = paragraphs[row_text][html_start:html_end]  # форматируемая часть текста
    # добавление форматирования в теги span
    span_style = ""
    span_style += f"color:{color};" if color else ""  # установить цвет?
    span_style += "font-weight:600;" if bold else ""  # сделать текст жирным?
    span_style += "font-style:italic;" if italic else ""  # сделать текст курсивом?
    span_style += "text-decoration: underline;" if underline else ""  # сделать текст подчёркнутым?
    insert_tag = [f"""<span style="{span_style}">""", """</span>"""]  # добавляемый тег span и прибавляем к нему стили
    paragraphs[row_text] = left_paragraph + insert_tag[0] + replacer_paragraph + insert_tag[1] + right_paragraph
    return html.replace("~***~", "\n".join(paragraphs))  # возвращаем обновленный html с примененным формат


if __name__ == '__main__':
    result = html_insert_tag(
        html=html_text, text=simple_text,
        num_par=2, start=1, end=1,  # номер параграфа / стартовый символ выделения / финишный символ выделения
        bold=True, italic=True, underline=True, color="#00ff00")
    print(result)
