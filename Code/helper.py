import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag

## HTML PARSER HELPER FUNCTIONS ##
# Open a BeautifulSoup object in a new tab
def open_soup(soup):
    html = str(soup)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)

# add style to element
def add_style(element, css_style,replace = False):
    if replace:
        element['style'] = css_style
    else:
        if element.get('style') is None:
            element['style'] = css_style
        else:
            element['style'] += ';' + css_style




# detects if text is bolded
def detect_bolded_text(element,recursive=True):
    style = element.get('style')
    if style:
        if 'font-weight:' in style:
            font_weight = element.get('style').split('font-weight:')[1].split(';')[0].strip()
            if font_weight == 'bold':
                return True
        
            # detect if font weight is integer above bold threshold
            elif font_weight.isdigit():
                if int(font_weight) > 500:
                    return True
    else:
        if element.name == 'b':
            return True

    # check children
    if recursive:
        descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
        if 'b' in [tag.name for tag in descendant_tags]:
            return True
    
    return False

# detects if text is italicized
def detect_italicized_text(element, recursive=True):
    style = element.get('style')
    if style:
        if 'font-style:' in element.get('style'):
            font_style = element.get('style').split('font-style:')[1].split(';')[0].strip() 
            if font_style == 'italic':
                return True
    else:
        if element.name == 'i':
            return True

    # check children
    if recursive:
        descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
        if 'b' in [tag.name for tag in descendant_tags]:
            return True
    
    return False

# detects if text is underlined
def detect_underlined_text(element, recursive=True):
    style = element.get('style')
    if style:
        if 'text-decoration:' in element.get('style'):
            text_decoration = element.get('style').split('text-decoration:')[1].split(';')[0].strip()
            if text_decoration == 'underline':
                return True
    else:
        if element.name == 'u':
            return True

    # check children
    if recursive:
        descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
        if 'b' in [tag.name for tag in descendant_tags]:
            return True
    
    return False



# clean html for parser
def clean_html(soup):
    # remove element-type attribute
    for element in soup.find_all(recursive=True):
        if element.has_attr("element-type"):
            del element['element-type']  

    # remove parsed attribute
    for element in soup.find_all(recursive=True):
        if element.has_attr("parsed"):
            del element['parsed']  

    # remove existing background colors
    for element in soup.find_all(recursive=True):
        if element.has_attr("style"):
            element['style'] = re.sub(r'background(-color)*:[^;]{1,}','',element['style'])

    # remove hidden elements
    for element in soup.select('[style*="display: none"]',recursive=True):
        element.decompose()
    for element in soup.select('[style*="display:none"]',recursive=True):
        element.decompose()



## XML PARSER HELPER FUNCTIONS ##