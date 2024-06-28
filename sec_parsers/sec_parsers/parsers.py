from time import time
from style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text
from xml_helper import get_text, set_background_color, remove_background_color


def recursive_parse(element):

    values = element.values()
    if len(values) == 1:
        if 'display:none' in values[0]:
            return

    if detect_table(element):
        # remove style from all children so that background color can be set
        for descendant in element.iterdescendants():
            remove_background_color(descendant)

        if detect_table_of_contents(element) == "toc":
            set_background_color(element, '#00FFFF')
        else:
            set_background_color(element, '#7FFF00')
        return

    if detect_link(element):
        set_background_color(element, '#7FFF00')
        return
    
    if detect_image(element):
        set_background_color(element, '#7FFF00')
        return

    text = get_text(element)
    if text == '':
        pass
    else:
        if detect_style_from_string(text) != 'no style found':
            set_background_color(element, '#FA8072')
        elif detect_style_from_element(element) != 'no style found':
            set_background_color(element, '#FA8072')
        else:
            pass


    for child in element.iterchildren():
        recursive_parse(child)

    return
        
