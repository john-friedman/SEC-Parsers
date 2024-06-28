from download import download_sec_filing
from lxml import etree, html
import re
import webbrowser
import tempfile
from time import time
from style_detection import detect_style


# implement lmxl parser - note: may have to abandon this approach as lxml might not deal with messy html well
# work on visualizer first

sec_html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1018724/000101872423000004/amzn-20221231.htm')

# preprocessing I WOULD LOVE TO REMOVE non breaking spaces, but I can't figure it out
sec_html = re.sub(r'\s+', ' ', sec_html)


parser = etree.HTMLParser(encoding='utf-8') # change to utf-8-sig
root = etree.fromstring(sec_html, parser)

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

# lookup what this is called
#tree  = etree.fromstring('<html> <body> <div>text1 <p> par1</p> text2 <p>par2</p> text3</div> </body> </html>', parser)


def get_text(element):
    """Get text from element including tail"""
    text = ''
    if element.text:
        text += element.text
    
    if element.tail:
        text += ' ' + element.tail
    return text

def get_all_text(element):
    """Get all text from element including children. Make include tail"""
    text = ''
    for child in element.iter():
        text += get_text(child)

    return text

def get_unique_parent_text(element):
    text = ''
    for child in element.iter():
        tail_text = child.tail
        if tail_text:
            text += tail_text
    return text

def find_node_by_text(node,text):
    """Find a node by its text"""
    xpath = f".//*[contains(text(), '{text}')]"
    node_with_text = node.xpath(xpath)
    return node_with_text


def clean_text(text):
    text = text.strip()
    return text

def clean_tag_name(text):
    text = text.lower()
    text = re.sub('\s+', '', text)
    return text

def detect_sentence(text):
    words = text.split()
    if len(words) > 5:
        if text[-1] == '.':
            return True
    return False

# visualize first. Once visualization is good, we'll add parsing to root
# first understand
def iterate_element(element,msg=''):

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
        if detect_style(text) != 'no style found':
            set_background_color(element, '#FA8072')
        else:
            pass


    s2 = time()
    return s2 - s1

    



body = root.find('body')
time = iterate_element(body)
print(time)
open_tree(root)

