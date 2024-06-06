from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import re
import os

from helper import open_soup, add_style, detect_bolded_text, detect_italicized_text, detect_underlined_text,clean_html

# TODO
# we need table parsing
# we need context detection, e.g. first content item is bold. - I can probably do this in tree extraction

def parse_element(element):
    
    # if no text, mark as empty
    if element.text.strip() == "":
        element['parsed'] = True
        element['element-type'] = f'{element.name}:empty'
        element['class'] = 'empty'
        return
    else:
        element['parsed'] = True
        element['element-type'] = f'{element.name}:text'
        element['class'] = 'section_text'
        if detect_bolded_text(element, recursive=False):
            element['element-type'] = 'bold;'
            element['class'] = 'header'

        if detect_italicized_text(element, recursive=False):
            element['element-type'] = 'italic;'
            element['class'] = 'header'
        
        if detect_underlined_text(element, recursive=False):
            element['element-type'] = 'underline;'
            element['class'] = 'header'

        return


def recursive_parser(element):
    """Will likely change name. Iterates through tree recursively and parses elements."""
    
    # check if element is a tag
    # this should be unnecessary
    if isinstance(element, Tag):

        # I need to add something for empty text
        if element.name in ['p','span','div','b','i']:
            element['parsed'] = True
            children = element.contents
            children_tags = [child for child in children if isinstance(child, Tag)]
            
            parse_element(element)

            if element['class'] == 'empty':
                return
            else:
                for child in children_tags:
                    recursive_parser(child)

            return

        # remove breaks
        elif element.name == 'br':
            element['parsed'] = True
            element['element-type'] = 'line-break:empty'
            return
        
        # remove table of contents
        elif element.name == 'a':
            element['parsed'] = True
            if element.text.strip().lower() == 'table of contents':
                element['element-type'] = 'a:toc-link'
                return
            
        # ignore tables for now
        elif element.name in ['table']:
            element['parsed'] = True
            element['element-type'] = 'table:skipping'
            return
        
        else:
            # i think we can safely ignore navigable strings
            children = [child for child in element.findChildren(recursive=False) if isinstance(child, Tag)]
            if len(children) > 0:
                for child in children:
                    recursive_parser(child)
            else:
                return
    
# we should probably mod this to add class?, e.g. class = section header / text?
# not sure
# also iterating through the tree so many times adds overhead.
# perhaps we should combine everything into one function, with multiple args
def color_parsing(soup):
    # https://www.htmlcodes.ws/color/html-color-code-generator.cfm?colorName=PowderBlue


    # we'll add gradient colors later in the distinguishing headers update
    color_dict = {'header':'BurlyWood','section_text':'Wheat','empty':'LightYellow','skipping':'LemonChiffon'}

    for element in soup.find_all(attrs={'element-type': True}):
        element_type = element['element-type']

        # there will be weird visualization errors here. This is sloppy
        if 'empty' in element_type:
            add_style(element, f"background-color:{color_dict['empty']};")
        elif (('bold' in element_type) | ('italic' in element_type) | ('underline' in element_type)):
            add_style(element, f"background-color:{color_dict['header']};")
        elif 'skipping' in element_type:
            add_style(element, f"background-color:{color_dict['skipping']};")
        else:
            add_style(element, f"background-color:{color_dict['section_text']};")
    
# code to test:
# load all 10-k files
dir_10k = "../Data/10K"
files = []
for file in os.listdir(dir_10k):
    files.append(f"{dir_10k}/{file}")


for file in files[0:5]:
    # may want to adjust encoding to utf-8-sig
    with open(file) as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    clean_html(body)
    recursive_parser(body)
    color_parsing(body)
    open_soup(soup)
