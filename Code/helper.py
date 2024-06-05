import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag

# anchors
def extract_text_before_anchor(elem_list,current_index,anchor_text):
    text_before_anchor = ""
    for idx,item in enumerate(elem_list[current_index:]):
            item_text = item.text
            text = item_text

        
            if text !="":
                text_before_anchor += text + ";"
            if anchor_text.lower() in text.lower():
                break

    text_before_anchor = re.sub(r"\s+", " ", text_before_anchor)
    current_index+= idx+1

    return current_index,text_before_anchor

def find_anchor(elem_list,current_index,anchor_text):
    idx, element = next(item for item in enumerate(elem_list[current_index:]) if anchor_text.lower() in item[1].text.lower())
    return current_index+idx, element

# text
# this will likely need work
def is_paragraph(element):
  
    text = element.text.strip()

    msg = ""
    # check if element is not blank
    if text == "":
        return False
    
    msg += "no blank text;"
    
    # check is not some massive div
    if len(element.findChildren()) > 10:
        return False
    
    msg += "not too many children;"

    # check if element is only numbers
    if re.search(r'^\d{1,}$', text):
        msg = "only numbers"
        return False
    
    msg += "not just numbers;"

    words = text.split()
    # check first letter of first word is uppercase
    if words[0][0].isupper():
        msg += "first letter is uppercase;"
        # check has a period
        search = re.search(r'\.',text)
        if search:
            msg += "has period;"
            if len(text) > 70:
                return True
            # check is above minimum length
            
    return False#, msg


# new approach, unique text becomes headers. one lower than each other
# maybe we build bottom up 
# detect low level text, check if special, then build up

# need a way to test if in paragraph, but not header within paragraph
def detect_unique_text(element):
    element_text = element.text.strip()

    # check if element is only special characters
    if re.match(r'^([\W_]|[0-9])+$', element_text):
        return False

    toReturn = False
    if element.name in ["strong","b","em","i","u"]:
        toReturn = True
    elif (element.get("style") is not None):
        if "bold" in element.get("style"):
            toReturn = True
        if "italic" in element.get("style"):
            toReturn = True
        if "underline" in element.get("style"):
            toReturn = True

    return toReturn

def detect_unique_text_deprecated(element):
    element_text = element.text.strip()

    # check if element is only special characters
    if re.match(r'^([\W_]|[0-9])+$', element_text):
        return False
    
    # check if all uppercase
    # haven't debugged yet
    if element_text.isupper():
        return True

    toReturn = False
    if (element.parent.name in ["strong","b","em","i","u"]):
        toReturn = True
    elif (element.name in ["strong","b","em","i","u"]):
        if element.parent.text.strip() == element_text:
            toReturn = True
    elif (element.get("style") is not None):
        if "bold" in element.get("style"):
            toReturn = True
        if "italic" in element.get("style"):
            toReturn = True
        if "underline" in element.get("style"):
            toReturn = True
        if 'text-align: center' in element.get("style"):
            toReturn = True
    
    # check if url
    # if is_valid_url(element_text):
    #     toReturn = False

    
    return toReturn

#beautiful soup

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
def detect_bolded_text(element):
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

    descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
    if 'b' in [tag.name for tag in descendant_tags]:
        return True
    
    return False
def detect_italicized_text(element):
    style = element.get('style')
    if style:
        if 'font-style:' in element.get('style'):
            font_style = element.get('style').split('font-style:')[1].split(';')[0]
            if font_style == 'italic':
                return True

    descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
    if 'i' in [tag.name for tag in descendant_tags]:
        return True
    
    return False

def detect_underlined_text(element):
    style = element.get('style')
    if style:
        if 'text-decoration:' in element.get('style'):
            text_decoration = element.get('style').split('text-decoration:')[1].split(';')[0]
            if text_decoration == 'underline':
                return True

    descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
    if 'u' in [tag.name for tag in descendant_tags]:
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
