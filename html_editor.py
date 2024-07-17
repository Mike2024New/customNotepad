import re


def html_insert_tag(html: str, num_par: int, start: int,
                    end: int, bold=False, italic=False, underline=False, color=None) -> str:
    """
    Добавление тега span со стилями форматирования в html коде
    :param num_par: номер параграфа
    :param start: стартовая позиция выделенного текста
    :param end: финишная позиция выделенного текста
    :param html: исходный html код
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

    # 2. поиск соответствия выделенн позиции в html (в теге p), для оптимиз алгоритма поиск ведется только в 1 строке
    html_start = None  # стартовая позиция выделенного слова в html коде
    html_end = None  # конечная позиция выделенного слова в html коде
    html_position_global = 0  # глобальный счётчик, считает все символы подряд
    html_position_local = 0  # локальный счётчик, считает только те символы которые вне html тегов (то есть текст)
    is_tag = True  # флаг, определяющий где находится цикл, внутри тега или снаружи (в контенте - тексте параграфа)
    is_spec_char = False  # иногда будут встречаться спецсимв типа &quot; их нужно обойти (прибавив 1 к global и local)

    for i in paragraphs[num_par]:
        """алгоритм обходит все символы абзаца, если символ находится в теге (is_tag), то обновить только глобальный
        счётчик символов, если символ(i), находится вне тега(в тексте), то обновить и глобальный и локальный счетчики
        таким образом достигается совпадение символов в простом тексте и html документе
        также добавлен обход спецсимволов типа &quot;"""
        if i == "<":  # точка открытия тега
            is_tag = True
        elif i == ">":  # точка закрытия тега
            is_tag = False
        elif i == "&":
            # если попался символ & это значит будет спецсимвол пропускать всё до тех пор пока не встретим ;
            is_spec_char = True  # устанавливать флаг который показывает что сейчас идёт код спецсимвола
            html_position_local += 1  # увеличить глобальную позицию на 1 (так как спесимвол обычно длиной 1)
            html_position_global += 1  # увеличить локальную позицию на 1 (так как спесимвол обычно длиной 1)
        elif i == ";" and is_spec_char:
            is_spec_char = False  # ; выход из спецсимвола
        if not is_tag and i != ">" and i != "<" and not is_spec_char:
            """если находится вне тега, то есть в самом контексте (тексте параграфа)"""
            if html_position_local == start:
                """если локальная позиция, совпадает с положением в простом тексте"""
                html_start = html_position_global
            elif html_position_local == end - 1:
                """если локальная позиция, совпадает с положением в простом тексте"""
                html_end = html_position_global + 1
            html_position_local += 1  # так как мы вне тега, то увеличиваем local на +1
        html_position_global += 1  # каждый символ подряд глобальный счётчик обновляется
    # если длина 1, то сделать коррекцию
    if end - start == 1:
        html_end = html_start + 1

    # сборка обновленного html
    print(f"html_start: {html_start} | html_end: {html_end}")
    left_paragraph = paragraphs[num_par][:html_start]  # часть параграфа до выделенного текста
    right_paragraph = paragraphs[num_par][html_end:]  # часть параграфа после выделенного текста
    replacer_paragraph = paragraphs[num_par][html_start:html_end]  # форматируемая часть текста
    # добавление форматирования в теги span
    span_style = ""
    span_style += f"color:{color};" if color else ""  # установить цвет?
    span_style += "font-weight:600;" if bold else ""  # сделать текст жирным?
    span_style += "font-style:italic;" if italic else ""  # сделать текст курсивом?
    span_style += "text-decoration: underline;" if underline else ""  # сделать текст подчёркнутым?
    insert_tag = [f"""<span style="{span_style}">""", """</span>"""]  # добавляемый тег span и прибавляем к нему стили
    paragraphs[num_par] = left_paragraph + insert_tag[0] + replacer_paragraph + insert_tag[1] + right_paragraph
    return html.replace("~***~", "\n".join(paragraphs))  # возвращаем обновленный html с примененным формат


if __name__ == '__main__':
    html_text = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Liberation Mono'; font-size:12pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">test text for example</p></body></html>"""
    result = html_insert_tag(
        html=html_text,
        num_par=0, start=10, end=13,  # номер параграфа / стартовый символ выделения / финишный символ выделения
        bold=True)
    # bold=True, italic=True, underline=True, color="#00ff00")
    print(result)
