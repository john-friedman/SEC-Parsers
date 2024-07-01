from time import time
from style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text
from xml_helper import get_text, set_background_color, remove_background_color, open_tree,check_if_is_first_child, element_has_text, element_has_tail
from lxml import etree
import re
from helper import headers_colors_dict, headers_colors_list

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

        # if no style found / pruning / cleaning
        if (string_style+element_style == ''):
            element.attrib['parsing'] = ''
        else:

            if any(style in element_style for style in ['font-weight:bold','font-weight:700;','b-tag;','strong-tag;']):
                parsing_string += 'bold-tag;'

            if any(style in element_style for style in ['font-style:italic','em','i']):
                parsing_string += 'italic-tag;'

            if any(style in element_style for style in ['text-decoration:underline','u']):
                parsing_string += 'underline-tag;'

            # change to functions
            if re.search('^item',get_all_text(element).strip(), re.IGNORECASE):
                parsing_string = 'item;'
                string_style = ''
            elif string_style == 'item;':
                parsing_string = 'item;'
                string_style = ''
            
            if re.search('^part',get_all_text(element).strip(), re.IGNORECASE):
                parsing_string = 'part;'
                string_style = ''

            #relative
            previous_element = element.getprevious()
            if previous_element is not None:
                if element_has_text(previous_element):
                    # change to go back further if empty?
                    previous_element_parsing_string = previous_element.attrib.get('parsing')
                    if previous_element_parsing_string == 'bullet point;':
                        string_style = ''
                        parsing_string = ''
                    elif previous_element_parsing_string == '':
                        string_style = ''
                        parsing_string = ''
                    elif previous_element_parsing_string == 'item;':
                        string_style = 'item;'
                        parsing_string = ''
                    elif previous_element_parsing_string == 'part;':
                        string_style = 'part;'
                        parsing_string = ''


            parsing_string += string_style

            if ((get_all_text(element) == '') and (element.tail is not None)):
                parent = element.getparent()
                parent.attrib['parsing'] = parsing_string + 'parent;'
            elif ((parsing_string == 'item;') and (element.tail is not None)):
                parent = element.getparent()
                parent.attrib['parsing'] = parsing_string + 'parent;'
            else:
                element.attrib['parsing'] = parsing_string



    return
        
# need to add static colors at some point
# palette for headings
# palette for identified stuff
def visualize_tree(root):
    # remove style from all descendants so that background color can be set
    for descendant in root.iterdescendants():
        remove_background_color(descendant)

    # find all elements with parsing attribute
    elements = root.xpath('//*[@parsing]')
    # get all unique parsing values
    parsing_values = list(set([element.attrib['parsing'] for element in elements]))
    # create a color dict
    color_dict =dict(zip(parsing_values, headers_colors_list[:len(parsing_values)])) 
    # replace color dict values with values from headers_colors_dict
    for key in headers_colors_dict.keys():
        color_dict[key] = headers_colors_dict[key]
    for element in elements:
        # get attribute parsing
        parsing = element.attrib['parsing']
        if parsing == '':
            pass
        else:
            color = color_dict[parsing]
            set_background_color(element, color)

    open_tree(root)


# start from part i to part 4 skipping signatures and intro
# function to decide hierarchy of headers
# function to create nodes
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
