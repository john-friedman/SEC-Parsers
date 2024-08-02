import re
from sec_parsers.xml_helper import get_all_text
from sec_parsers.cleaning import clean_string_for_style_detection, part_pattern

#TODO happy with this file so far

# simple for now
def is_paragraph(text):
    periods = text.count('.')
    commas = text.count(',')
    if periods > 0:
        return True
    
    return False

# TODO: improve this
def detect_bullet_point(string):
    """e.g. •"""
    if any(char in string.strip() for char in ['•','●','●','●','●','•','·','◦']):
        return True
    return False

def detect_signatures(string):
    """e.g. Signatures"""
    match = re.search(r"^SIGNATURES$",string, re.IGNORECASE)
    if match:
        return True
    
    return False

def detect_item(string):
    """e.g. Item 1A. Risk Factors"""
    match = re.search(r"^Item\s+\d+[A-Z]{0,}",string, re.IGNORECASE)
    if match:
        return True
    return False

def detect_emphasis_capitalization(string): # WIP
    """Seen in amazon's 2024 10k e.g. We Have Foreign Exchange Risk"""
    # Check for None, None., Omitted., Not Applicable.
    if string.lower() in [item.lower() for item in ['None','None.','Omitted.', 'Not Applicable.']]:
        return False
    
    # if one word return false
    if len(string.split()) == 1:
        return False
    
    # if all caps
    if string.isupper():
        return False
    
    # Check if string is all digits
    if string.isdigit():
        return False
    
    words = string.split()
    if not words:
        return False

    has_capitalized_word = False
    for word in words:
        # Skip prepositions, articles, and conjunctions
        if word.lower() in ["of",'to','a','and','by','in','the','or','on','for','as','with','that','but','not','so','yet','an','at','off','per','up','via']:
            continue
        
        # Check if the word contains any alphabetic characters
        if any(char.isalpha() for char in word):
            if word[0].isupper():
                has_capitalized_word = True
            else:
                return False
        # If the word is just digits or punctuation, ignore it

    return has_capitalized_word
    
def detect_prospectus(string):
    """e.g. PROSPECTUS SUMMARY"""
    match = re.search(r"^PROSPECTUS SUMMARY$",string, re.IGNORECASE)
    if match:
        return True
    return False    

def detect_part(string):
    """e.g. Part I"""
    match = part_pattern.match(string.lower().strip())
    if match:
        return True
    return False
    
# deprecated for now
def level_detection(string):
    """e.g. amazon Level 1"""
    match = re.search(r"^Level\s+\d+",string)
    if match:
        return True
    return False
    

def detect_note(string):
    """e.g. Note 1"""
    match = re.search(r"^Note\s+\d+",string, re.IGNORECASE)
    if match:
        return True
    return False

def detect_all_caps(string):
    """e.g. FORM 10-K SUMMARY"""
    if string.isupper():
        return True
    # may cause issue
    elif string.isdigit():
        return True
    return False

def detect_page_number(string):
    if re.search(r"^\d+$",string, re.IGNORECASE):
        return True
    elif re.search(r'F-\d+$',string, re.IGNORECASE):
        return True
    else:
        return False

def detect_style_from_string(string):
    
    # PREPROCESSING WIP
    string = clean_string_for_style_detection(string)
    # ORDER MATTERS
    if detect_part(string):
        return 'part;'
    elif detect_item(string):
        return 'item;'
    elif detect_signatures(string):
        return 'signatures;'
    elif detect_page_number(string):
        return 'page number;'
    elif detect_bullet_point(string):
        return 'bullet point;'
    elif detect_all_caps(string):
        return 'all caps;'
    elif detect_emphasis_capitalization(string):
        return 'emphasis;'
    elif detect_note(string):
        return 'note;'
    else:
        return ''
    

def detect_hidden_element(element):
    if element.get('style'):
        if 'display:none' in re.sub(' ','',element.get('style')):
            return True
    return False

def detect_link(node):
    """Detects if a node is a link."""
    if node.tag == 'a':
        return True
    return False

def detect_bold_from_html(element):
    """Detects bold from html tags"""
    tag_list = ['b']
    if element.tag in tag_list:
        return True
    return False

def detect_strong_from_html(element):
    """Detects strong from html tags"""
    tag_list = ['strong']
    if element.tag in tag_list:
        return True
    return False

def detect_emphasis_from_html(element):
    """Detects emphasis from html tags"""
    tag_list = ['em']
    if element.tag in tag_list:
        return True
    return False

def detect_italic_from_html(element):
    """Detects italic from html tags"""
    tag_list = ['i']
    if element.tag in tag_list:
        return True
    return False

def detect_underline_from_html(element):
    """Detects underline from html tags"""
    tag_list = ['u']
    if element.tag in tag_list:
        return True
    return False

# deprecated
def detect_from_html(element):
    element_style = ''
    ancestors = list(element.iterancestors())
    # include self
    ancestors = ancestors + [element]
    # detect bold from ancestors
    for ancestor in ancestors:
        tag_list = ['b','strong','em','i','u']
        if ancestor.tag in tag_list:
            element_style += f'{ancestor.tag}-tag;'
        
    return element_style


# WIP, may need modification for different font weights
def detect_bold_from_css(element):
    """Detects bold from css"""
    if element.get('style'):
        if 'font-weight:bold' in element.get('style'):
            return True
        # change to be any font weight greater than 400
        elif 'font-weight:700' in element.get('style'):
            return True
    return False



def detect_underline_from_css(element):
    """Detects underline from css"""
    if element.get('style'):
        if 'text-decoration:underline' in element.get('style'):
            return True
    return False

def detect_italic_from_css(element):
    """Detects italic from css"""
    if element.get('style'):
        if 'font-style:italic' in element.get('style'):
            return True
    return False


def detect_style_from_element(element):
    # check it or descendants have text
    text = get_all_text(element).strip() # WIP DOES THIS MATTER? WE WILL SEE
    if len(text) == 0:
        return ''

    
    style = ''
    style += detect_bold_from_css(element)
    style += detect_from_html(element)
    style += detect_underline_from_css(element)
    style += detect_italic_from_css(element)
    style += detect_link(element)
    return style

def is_descendant_of_table(element):
    return bool(element.xpath("./ancestor::table"))

# needs work 
def detect_table(table):
    """Detects if table or header disguised as a table"""
    if table.tag != 'table':
        return False
    
    # this doesn't work
    #tr_list = table.xpath('//tr')

    tr_list = table.findall('tr')
    if len(tr_list) > 3:
        return True
    text = get_all_text(table)

    if detect_bullet_point(text):
        return False
    number_count = len(re.findall(r'\d', text))
    if number_count > 5:
        return True
    
    char_count = len(text)
    if char_count > 400:
        return True
    
    return False


def detect_table_of_contents(element):
    toc_type = 'not-toc'
    """Detects if a table is likely to be a table of contents."""

    # toc - needs seperate parser if no links
    num_items = len(re.findall(r'Item(\s+|$|\n)', get_all_text(element), re.IGNORECASE))
    if num_items > 9:
        toc_type = 'toc'

    # linked toc
    # links = element.find_all('a')
    # if len(links) > 5:
    #     toc_type = 'toc-links'

    return toc_type

def detect_toc_link(node):
    """Detects if a node is a table of contents link."""
    if node.tag == 'a':
        text = get_all_text(node)
        if text.lower() in ['table of contents','toc']:
            return True
    return False

def detect_image(node):
    """Detects if a node is an image."""
    if node.tag == 'img':
        return True
    return False

def detect_empty_string(string):
    return bool(re.match(r'^\s*$', string))

