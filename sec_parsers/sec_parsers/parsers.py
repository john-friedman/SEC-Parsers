from time import time
from style_detection import detect_style_from_string, detect_style_from_element, detect_table,detect_link, detect_image,detect_table_of_contents, get_all_text, is_paragraph
from xml_helper import get_text, set_background_color, remove_background_color, open_tree,check_if_is_first_child, element_has_text, element_has_tail,get_text_between_elements,get_elements_between_elements
from lxml import etree
import re
from visualization_helper import headers_colors_dict, headers_colors_list
from helper import get_hierarchy_from_lists, get_preceding_elements, find_last_index

def recursive_parse(element):
    # check if visible
    style = element.attrib.get('style')
    if style is not None:
        if 'display:none' in re.sub(' ','',style):
            return

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

            # check for items after risk factor which are text, but in italics
            if ((parsing_string == 'italic-tag;') and (is_paragraph(text))):
                parsing_string = ''
                string_style = ''

            # change this to functions
            if re.search('^item',get_all_text(element).strip(), re.IGNORECASE):
                parsing_string = 'item;'
                string_style = ''
            elif string_style == 'item;':
                parsing_string = 'item;'
                string_style = ''
            
            if re.search('^part',get_all_text(element).strip(), re.IGNORECASE):
                parsing_string = 'part;'
                string_style = ''

            if re.search('^SIGNATURES$',get_all_text(element).strip()):
                parsing_string = 'signature;'
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


# this is heavily WIP
def construct_xml_tree(parsed_html):
    """Constructs an xml tree from a parsed html file"""
    # initializes root
    root = etree.Element('root')
    root.attrib['parsing'] = 'root;'

    # find all parsing elements
    elements = parsed_html.xpath('//*[@parsing]')
    # subset by elements where parsing is not empty
    elements = [element for element in elements if element.attrib['parsing'] != '']
    # find the first part parsing
    first_part_element = [element for element in elements if element.attrib['parsing'] == 'part;'][0]
    # find signatures
    signature = [element for element in elements if element.attrib['parsing'] == 'signature;'][0]

    # subset elements between first part and signature
    elements = elements[elements.index(first_part_element):elements.index(signature)]
    # add the signature to the end of the elements
    elements.append(signature)

    element_parsing_strings = [element.attrib['parsing'] for element in elements]
    hierearchy = get_hierarchy_from_lists(element_parsing_strings)
    
    # fix here. we accidentally did next, instead of previous
    count = 0
    while count < len(elements)-1:
        element = elements[count]
        next_element = elements[count+1]

        element_parsing_string = element.attrib['parsing']

        # remove parent from parsing string
        element_parsing_string = re.sub('parent;','',element_parsing_string)

        desc = get_all_text(element)
        title = re.sub(' ','',desc.strip().lower())
        text = get_text_between_elements(parsed_html,element, next_element)
        if element_parsing_string == 'part;':
            node_class = 'part'
        elif element_parsing_string == 'item;':
            node_class = 'item'
        else:
            node_class = 'section'

        node = etree.Element(node_class, title = title, desc= desc, text = text, parsing = element_parsing_string)
        rulers = get_preceding_elements(hierearchy, element_parsing_string)


        tree = [node for node in root.iterdescendants()]
        node_hierachy_parsing_strings = [node.attrib['parsing'] for node in tree]
        # find the last element in the node_hierachy_parsing_strings which is in rulers
        index = find_last_index(node_hierachy_parsing_strings, rulers)
        if index == 0:
            root.append(node)
        else:
            tree[index-1].append(node)
            
        count += 1

    return root