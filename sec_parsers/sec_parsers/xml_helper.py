import webbrowser
import tempfile
from lxml import html, etree
import re

def find_by_text(node, text):
    """Find a node by text."""
    return node.xpath(f"//*[contains(text(), '{text}')]")

# need to think logic here through
# need opposite of tail

# checks if parent has text before any element. if it has text after element that shows up in childs tail
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

def open_tree(tree):
    """Opens a lxml tree in a web browser."""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        data = html.tostring(tree).decode("utf-8-sig")
        f.write(data)

    url = 'file://' + f.name
    webbrowser.open(url)

def print_tree(root):
    """Prints a lxml tree."""
    print(etree.tostring(root, pretty_print=True))