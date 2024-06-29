from time import time
from style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text
from xml_helper import get_text, set_background_color, remove_background_color, open_tree


def recursive_parse(element):

    values = element.values()
    if len(values) == 1:
        if 'display:none' in values[0]:
            return

    if detect_table(element):
        if detect_table_of_contents(element) == "toc":
            element.attrib['parsing'] = 'table of contents;'
        else:
            element.attrib['parsing'] = 'table;'
        return

    if detect_link(element):
        element.attrib['parsing'] = 'link;'
        return
    
    if detect_image(element):
        element.attrib['parsing'] = 'image;'
        return

    text = get_text(element)
    if text == '':
        pass
    else:
        if element.attrib.get('parsing') == None:
            element.attrib['parsing'] = ''
        string_style = detect_style_from_string(text)
        element_style = detect_style_from_element(element)
        if string_style != 'no style found':
            element.attrib['parsing'] += string_style

        if element_style != '':
            element.attrib['parsing'] += element_style


    for child in element.iterchildren():
        recursive_parse(child)

    return
        
# split visualization for now
def visualize_tree(root):
    # remove style from all descendants so that background color can be set
    for descendant in root.iterdescendants():
        remove_background_color(descendant)

    # find all elements with parsing attribute
    elements = root.xpath('//*[@parsing]')
    for element in elements:

        # get attribute parsing
        parsing = element.attrib['parsing']
        if parsing == 'table of contents;':
            set_background_color(element, '#00FFFF')
        elif parsing == 'table;':
            set_background_color(element, '#7FFF00')
        elif parsing == 'link;':
            set_background_color(element, '#7FFF00')
        elif parsing == 'image;':
            set_background_color(element, '#7FFF00')
        elif parsing == 'bullet point;':
            set_background_color(element, '#A9A9A9')
        elif parsing == '':
            pass
        else:
            set_background_color(element, '#FA8072')

    open_tree(root)
