import webbrowser
import tempfile
from lxml import html, etree
import re

# TODO: lookover and refactor

# unused
def get_highest_level_parent(element):
    """get ancestor before body"""
    ancestor = element
    while ancestor.getparent().tag != 'body':
        ancestor = ancestor.getparent()
    return ancestor

# need to rewrite considerable
# how about, if same parent, and next to each other, but parsing type prev is not there, then it is a middle element. done
# need to account for span inside p, etc.
def is_middle_element(elem):
    parent = elem.getparent()
    if parent is None:
        return False
    
    parent_text = parent.text.strip() if parent.text else ''
    if parent_text != '':
        return True
    
    previous_element = elem.getprevious()
    if previous_element is None:
        return False
    
    if previous_element.attrib.get('parsing_type','') == '':
        return True
    
    return False
    # parent = elem.getparent()
    # if parent is None:
    #     return False
    
    # parent_text = parent.text.strip() if parent.text else ''
    # parent_tail = parent.tail.strip() if parent.tail else ''
    # if (parent_text == ''):
    #     return False
    # else:
    #     return True

# cause of speed issues. Not sure if there is a better way to do this. Tried xpath, preprocessing, etc. preprocessing sometimes won, but usually was slower.
# may have to ask for help.
def get_elements_between_elements(root, start_element=None, end_element=None):
    """WIP"""
    elements = []
    in_between_bool = False
    for element in root.iter():
        if element.get('parsing_type','') == 'remove':
            continue
        
        if element == start_element:
            in_between_bool = True
        elif element == end_element:
            return elements
        elif in_between_bool:
            elements.append(element)

    return elements

def get_text_between_elements(root, start_element=None, end_element=None):
    """TODO: format text nicer"""
    elements = get_elements_between_elements(root, start_element, end_element)
    text = ""
    for element in elements:
        element_text = get_text(element).strip()
        if element_text != '':
            text += element_text + '\n'

    return text

# used for parsed html #

def element_has_text(element):
    text = element.text
    if text:
        text = text.strip()
        if text != '':
            return True
    return False

def element_has_tail(element):
    tail = element.tail
    if tail:
        tail = tail.strip()
        if tail != '':
            return True
    return False

def check_if_is_first_child(element):
    """Get first child of element"""
    previous_element = element.getprevious()

    if previous_element is None:
        parent = element.getparent()
        if not element_has_text(parent):
            return True
        else:
            return False
    elif len(previous_element.getchildren()) > 0:
        return False

    return False
    
def get_text(element):
    """Get text from element including tail"""
    text = ''
    if element.text:
        text += element.text

    if element.tail:
        text += ' ' + element.tail
    return text

# check includes tail
def get_all_text(node):
    """Get all text from element including children. Make include tail"""
    text = ''.join(node.itertext())

    return text


# visualization
def remove_style(element):
    """Removes the style attribute from an element."""
    element.attrib.pop('style', None)

def remove_background_color(element):
    """Removes the background color from an element."""
    current_style = element.get('style')
    if current_style:
        # remove background color from style if exists
        current_style = re.sub(r'background-color:.*?($|;)','',current_style)
        element.set('style', current_style)
    else:
        element.set('style', '')

def set_background_color(element, color):
    """Sets the background color for an element."""
    current_style = element.get('style')
    if current_style:
        new_style = f'{current_style}; background-color: {color}'
        element.set('style', new_style)
    else:
        element.set('style', f'background-color: {color}')
    
def remove_background(element):
    return

# Visualization #

def open_tree(tree):
    """Opens a lxml tree in a web browser."""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        data = html.tostring(tree).decode("utf-8-sig")
        f.write(data)

    url = 'file://' + f.name
    webbrowser.open(url)
