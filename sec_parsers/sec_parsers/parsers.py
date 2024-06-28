from time import time
from style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image
from xml_helper import get_text, set_background_color
# visualize first. Once visualization is good, we'll add parsing to root
# first understand
def iterate_element(element,msg=''):

    # skipping some elements
    
    if detect_table(element):
        # add something here to wipe existing background color
        set_background_color(element, '#7FFF00')
        return
    
    if detect_link(element):
        set_background_color(element, '#7FFF00')
        return
    
    if detect_image(element):
        set_background_color(element, '#7FFF00')
        return

    values = element.values()
    if len(values) == 1:
        if 'display:none' in values[0]:
            return

    s1 = time()
    children = element.getchildren()
    for child_idx, child in enumerate(children):
        if len(children) == 1:
            iterate_element(child,'only child')
        elif child_idx == 0:
            iterate_element(child,'first child')
        else:
            iterate_element(child,'')
    
    next_element = element.getnext()
    if next_element:
        iterate_element(next_element)
    
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


    s2 = time()
    return s2 - s1

