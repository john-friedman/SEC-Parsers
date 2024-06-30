from time import time
from style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text
from xml_helper import get_text, set_background_color, remove_background_color, open_tree,check_if_is_first_child, element_has_text, element_has_tail
from lxml import etree
import re

# add item and part detection
def recursive_parse(element):
    if element.attrib.get('parsing') == None:
        element.attrib['parsing'] = ''

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

    text = get_text(element).strip()
    if text == '':
        for child in element.iterchildren():
            recursive_parse(child)
    else:
        string_style = detect_style_from_string(text)
        element_style = detect_style_from_element(element)
        parsing_string = ''
        if string_style != 'no style found':
            parsing_string += string_style

        if element_style != '':
            parsing_string+= element_style

        # if no style found / pruning / cleaning
        if parsing_string == '':
            element.attrib['parsing'] = ''
        else:
            previous_element = element.getprevious()
            if previous_element is not None:
                if element_has_text(previous_element):
                    previous_element_parsing_string = previous_element.attrib.get('parsing')
                    if previous_element_parsing_string == 'bullet point;':
                        parsing_string = ''
                    elif previous_element_parsing_string == '':
                        parsing_string = ''

            # check if item
            if re.search('^item',get_all_text(element).strip(), re.IGNORECASE):
                parsing_string = 'item;'
            elif re.search('^part',get_all_text(element).strip(), re.IGNORECASE):
                parsing_string = 'part;'

            # will this work?
            if ((get_all_text(element) == '') and (element.tail is not None)):
                parent = element.getparent()
                parent.attrib['parsing'] = parsing_string
            else:
                element.attrib['parsing'] = parsing_string



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
        if parsing == 'part;':
            set_background_color(element, '#FA8072')
        elif parsing == 'item;':
            set_background_color(element, '#FFA500')
        elif parsing == 'table of contents;':
            set_background_color(element, '#00FFFF')
        elif parsing == 'table;':
            set_background_color(element, '#D8BFD8')
        elif parsing == 'link;':
            set_background_color(element, '#D8BFD8')
        elif parsing == 'image;':
            set_background_color(element, '#D8BFD8')
        elif parsing == 'bullet point;':
            set_background_color(element, '#A9A9A9')
        elif parsing == 'page number;':
            set_background_color(element, '#D8BFD8')
        elif parsing == '':
            pass
        else:
            set_background_color(element, '#FFD700')

    open_tree(root)


# start from part i to part 4 skipping signatures and intro
# logic: part then item

# start code sloppy then fix
def construct_xml_tree(parsed_html):
    root = etree.Element('root')

    # find all parsing elements
    elements = parsed_html.xpath('//*[@parsing]')
    # select elements with parsing attribute
    parse_bool = False
    for idx,element in enumerate(elements):
        parsing = element.attrib['parsing']
        text = get_text(element).strip()
        
        if text ==  'PART I':
            parse_bool = True
        elif text == 'SIGNATURES':
            parse_bool = False

        if parse_bool:
            if parsing == 'part;':
                part_node = etree.SubElement(root, "part", title=text)
            elif parsing == 'item;':
                item_node = etree.SubElement(part_node, "item", title=text)

    return root
