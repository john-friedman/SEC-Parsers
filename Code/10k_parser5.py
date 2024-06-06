from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import re
import os

from helper import open_soup, add_style, detect_bolded_text, detect_italicized_text, detect_underlined_text,clean_html

# TODO
# I think it's pretty good, we just need to work on tree creation, the context dependent stuff there
# will help us fix visuals

# need to adjust. if element has no text of its own, it should be ignored
def parse_element(element,recursive=False):

    contents = element.contents
    navigable_strings = [child for child in contents if isinstance(child, NavigableString)]
    if len(navigable_strings) == 0:
        element['class'] = 'container-no-text'
        return
    
    # if no text, mark as empty
    elif element.text.strip() == "":
        element['parsed'] = True
        element['element-type'] = f'{element.name}:empty'
        element['class'] = 'empty'
        return
    else:
        element['parsed'] = True
        element['element-type'] = f'{element.name}:text'
        element['class'] = 'section_text'
        if detect_bolded_text(element, recursive):
            element['element-type'] = 'bold;'
            element['class'] = 'header'

        if detect_italicized_text(element, recursive):
            element['element-type'] = 'italic;'
            element['class'] = 'header'
        
        if detect_underlined_text(element, recursive):
            element['element-type'] = 'underline;'
            element['class'] = 'header'

        return
    

# need better table detection
# table detection is very sloppy
def parse_table(element):
    
    tr_list = element.find_all('tr')
    if any([re.search(r'[0-9]{1,},[0-9]{1,}', tr.text) for tr in tr_list]) :
        element['parsed'] = True
        element['element-type'] = 'table:numeric'
        element['class'] = 'skipping'
        return
    elif len([re.search(r'^[0-9]{1,}$', tr.text) for tr in tr_list]) > 5:
        element['parsed'] = True
        element['element-type'] = 'table:numeric'
        element['class'] = 'skipping'
        return
    elif len([re.search(r'[1-2][0-9]{3}', tr.text) for tr in tr_list]) > 3:
        element['parsed'] = True
        element['element-type'] = 'table:numeric'
        element['class'] = 'skipping'
        return
    
    for tr in tr_list:
        td_list = tr.find_all('td')
        for td in td_list:
            recursive_parser(tr)

     

def recursive_parser(element):
    """Will likely change name. Iterates through tree recursively and parses elements."""
    
    # check if element is a tag
    # this should be unnecessary
    if isinstance(element, Tag):

        # I need to add something for empty text
        if ((element.name in ['p','span','div','b','i','td']) | ('ix' in element.name)):
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
            element['class'] = 'empty'
            return
        
        # remove table of contents
        elif element.name == 'a':
            element['parsed'] = True
            if element.text.strip().lower() == 'table of contents':
                element['element-type'] = 'a:toc-link'
                element['class'] = 'skipping'
                return
            
        # ignore tables for now
        elif element.name in ['table']:
            parse_table(element)
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
    color_dict = {'header':'BurlyWood','section_text':'Wheat','empty':'LightYellow','skipping':'Pink'}

    for element in soup.find_all(attrs={'class': True}):
        element_class = element['class']

        # there will be weird visualization errors here. This is sloppy
        if element_class == 'empty':
            add_style(element, f"background-color:{color_dict['empty']};")
        elif element_class == 'header':
            add_style(element, f"background-color:{color_dict['header']};")
        elif element_class == 'skipping':
            add_style(element, f"background-color:{color_dict['skipping']};")
        elif element_class == 'section_text':
            add_style(element, f"background-color:{color_dict['section_text']};")
    
# code to test:
# load all 10-k files
dir_10k = "../Data/10K"
files = []
for file in os.listdir(dir_10k):
    files.append(f"{dir_10k}/{file}")


for file in files[0:3]:
    # may want to adjust encoding to utf-8-sig
    with open(file) as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    clean_html(body)
    recursive_parser(body)
    color_parsing(body)
    open_soup(soup)
