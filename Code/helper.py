import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag


def open_soup(soup):
    html = str(soup)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)


# go through children recustively, if no text, decompose item
def clean_element(element):
    # check if element exists
    if element.name is None:
        return
    # handle table of contents
    elif element.name == "a":
        if element.text.strip().lower() == 'table of contents':
            element.decompose()
    # handle empty elements
    elif element.text.strip() == "":
        element.decompose()
    # if has children apply recursively
    elif len(element.findChildren())>0:
        for child in element.children:
                        clean_element(child)
    # if no children remove line breaks
    else:
        pass

# quick fix
def combine_elements(element):
    if element.name is None:
        return
    # arbitary, this will break?
    # need to add something here that takes into account weird normal c bold ompetition. I think the best way is to weight style.
    if ((len(element.contents) < 100) & (len(element.contents) > 1)):
        element.string = re.sub(r'[(\n)(\s+)]{1,}',' ',element.text.strip())
    for child in element.children:
        combine_elements(child)
        


def mark_unique_text(element):
    if element.name is None:
        return
    if detect_unique_text(element):
        add_style(element, "background-color:SandyBrown;")
    for child in element.children:
        mark_unique_text(child)

# change to account for ';'
def add_style(element, css_style,replace = False):
    if replace:
        element['style'] = css_style
    else:
        if element.get('style') is None:
            element['style'] = css_style
        else:
            element['style'] += ';' + css_style



def add_text(element, text):
    if element.get('text') is None:
        element.append(text)

def add_class(element, class_string):
    if element.get('class') is None:
        element['class'] = class_string
    else:
        pass

def check_if_ancestor_has_class(element):
    element_parent = element.parent
    while element_parent.name != "html":
        if element_parent.has_attr("class"):
            return True
        element_parent = element_parent.parent
    
    return False



# rewrite as of june 4
def detect_bolded_text(element,recursive=True):
    style = element.get('style')
    if style:
        if 'font-weight:' in style:
            font_weight = element.get('style').split('font-weight:')[1].split(';')[0].strip()
            if font_weight == 'bold':
                return True
        
            # detect if font weight is integer
            elif font_weight.isdigit():
                if int(font_weight) > 500:
                    return True

    # check children
    if recursive:
        descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
        if 'b' in [tag.name for tag in descendant_tags]:
            return True
    
    return False
def detect_italicized_text(element, recursive=True):
    style = element.get('style')
    if style:
        if 'font-style:' in element.get('style'):
            font_style = element.get('style').split('font-style:')[1].split(';')[0].strip() 
            if font_style == 'italic':
                return True

    # check children
    if recursive:
        descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
        if 'b' in [tag.name for tag in descendant_tags]:
            return True
    
    return False

def detect_underlined_text(element, recursive=True):
    style = element.get('style')
    if style:
        if 'text-decoration:' in element.get('style'):
            text_decoration = element.get('style').split('text-decoration:')[1].split(';')[0].strip()
            if text_decoration == 'underline':
                return True

    # check children
    if recursive:
        descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
        if 'b' in [tag.name for tag in descendant_tags]:
            return True
    
    return False

# simplify 10k
def add_element(element,soup):
    soup.append(element)

    # add line breaks twice
    for _ in range(2):
        line_break = soup.new_tag('br')
        line_break['element-type'] = 'line-break'
        soup.append(line_break)
