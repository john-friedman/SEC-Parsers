import webbrowser
import tempfile
from lxml import html


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

def set_background_color(element, color):
    """Sets the background color for an element."""
    element.set('style', f'background-color: {color}')

def open_tree(tree):
    """Opens a lxml tree in a web browser."""
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        data = html.tostring(tree).decode("utf-8-sig")
        f.write(data)

    url = 'file://' + f.name
    webbrowser.open(url)