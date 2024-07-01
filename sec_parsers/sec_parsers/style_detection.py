import re
from xml_helper import get_all_text

# simple for now
def is_paragraph(text):
    periods = text.count('.')
    commas = text.count(',')
    if periods > 0:
        return True
    
    return False

def detect_bullet_point(string):
    """e.g. •"""
    if any(char in string.strip() for char in ['•','●','●','●','●']):
        return True
    return False

def detect_style_from_string(string):
    def detect_emphasis_capitalization(string):
        """Seen in amazon's 2024 10k e.g. We Have Foreign Exchange Risk"""
        if string in ['None','None.','Omitted.']:
            return False
        
        words = string.split()
        if not words:
            return False
        for word in words:
            if word.lower() in ["of",'to','a','and','by','in','the','or','on','for','as','with','that','but','not','so','yet','an','at','off','per','up','via']:
                continue
            # check for numbers, e.g. 2021, but not ITEM2021. ITEM2021 counts as upper
            elif not any(char.isalpha() for char in word):
                continue

            if not word[0].isupper():
                return False
        return True
    
    def detect_item(string):
        """e.g. Item 1A. Risk Factors"""
        match = re.search(r"^Item\s+\d+[A-Z]{0,}",string, re.IGNORECASE)
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
        

    def note_detection(string):
        """e.g. Note 1"""
        match = re.search(r"^Note\s+\d+",string, re.IGNORECASE)
        if match:
            return True
        return False
    
    def all_caps(string):
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
    
    if detect_page_number(string):
        return 'page number;'
    elif all_caps(string):
        return 'all caps;'
    elif detect_emphasis_capitalization(string):
        return 'emphasis;'
    elif detect_item(string):
        return 'item;'
    elif note_detection(string):
        return 'note;'
    elif detect_bullet_point(string):
        return 'bullet point;'
    else:
        return ''
    
def detect_style_from_element(element):
    def detect_bold_from_css(element):
        """Detects bold from css"""
        if element.get('style'):
            if 'font-weight:bold' in element.get('style'):
                return 'font-weight:bold;'
            # change to be any font weight greater than 400
            elif 'font-weight:700' in element.get('style'):
                return 'font-weight:700;'
        return ''
    
    def detect_from_html(element):
        ancestors = list(element.iterancestors())
        # include self
        ancestors = ancestors + [element]
        # detect bold from ancestors
        for ancestor in ancestors:
            tag_list = ['b','strong','em','i','u']
            if ancestor.tag in tag_list:
                return f'{ancestor.tag}-tag;'
            
        return ''
    
    def detect_underline_from_css(element):
        """Detects underline from css"""
        if element.get('style'):
            if 'text-decoration:underline' in element.get('style'):
                return 'text-decoration:underline;'
        return ''
    
    def detect_italic_from_css(element):
        """Detects italic from css"""
        if element.get('style'):
            if 'font-style:italic' in element.get('style'):
                return 'font-style:italic;'
        return ''
    
    
    # check it or descendants have text
    text = get_all_text(element).strip()
    if len(text) == 0:
        return ''

    
    style = ''
    style += detect_bold_from_css(element)
    style += detect_from_html(element)
    style += detect_underline_from_css(element)
    style += detect_italic_from_css(element)
    return style
    

# needs work 
def detect_table(table):
    """Detects if table or header disguised as a table"""
    if table.tag != 'table':
        return False
    
    tr_list = table.xpath('//tr')
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
    num_items = len(re.findall('Item(\s+|$|\n)', get_all_text(element), re.IGNORECASE))
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

def detect_link(node):
    """Detects if a node is a link."""
    if node.tag == 'a':
        return True
    return False

def detect_image(node):
    """Detects if a node is an image."""
    if node.tag == 'img':
        return True
    return False