from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import re
import os

from helper import open_soup, add_style, detect_bolded_text, detect_italicized_text, detect_underlined_text

# TODO
# further parsing, e.g. table, for real tables
# building the tree


def clean_html(soup):
    # reminder to look for element-type, as we will be using that attribute
    for element in body.find_all():
        if element.has_attr("element-type"):
            del element['element-type']  

    # remove existing background colors from all elements
    # Note: coded this quickly using copilot, did not check
    for element in body.find_all():
        if element.has_attr("style"):
            element['style'] = re.sub(r'background-color:[^;]{1,}','',element['style'])

    # remove hidden elements
    # may need to tweak
    for element in body.select('[style*="display: none"]'):
        element.decompose()
    for element in body.select('[style*="display:none"]'):
        element.decompose()


def recursive_parser(element):
    """Will likely change name. Iterates through tree recursively and parses elements."""
    
    # check if element is a tag
    if isinstance(element, Tag):
        # Parse specific tags

        # parses p
        if element.name == 'p':
            # check is p is empty
            if element.text.strip() == "":
                element['element-type'] = 'p:empty'
                return
            else:
                element['element-type'] = 'p:'

                if detect_bolded_text(element):
                    element['element-type'] += 'bold;'

                if detect_italicized_text(element):
                    element['element-type'] += 'italic;'

                if detect_underlined_text(element):
                    element['element-type'] += 'underline;'
                
                return
        elif element.name == 'span':
            if element.text.strip() == "":
                element['element-type'] = 'span:empty'
                return
            else:
                element['element-type'] = 'span:'

                if detect_bolded_text(element):
                    element['element-type'] += 'bold;'

                if detect_italicized_text(element):
                    element['element-type'] += 'italic;'

                if detect_underlined_text(element):
                    element['element-type'] += 'underline;'

                return
        # remove breaks
        elif element.name == 'br':
            element['element-type'] = 'line-break:empty'
            return
        # remove table of contents
        elif element.name == 'a':
            if element.text.strip().lower() == 'table of contents':
                element['element-type'] = 'a:toc-link'
                return
        # ignore tables for now
        elif element.name in ['table']:
                element['element-type'] = 'table:skipping'
                return
        # parses div. THIS IS HARD
        # fix container parsing for bold etc
        elif element.name == 'div':
            children = [child for child in element.findChildren(recursive=False) if isinstance(child, Tag)]
            if len(children) == 0:
                element['element-type'] = 'div:'
                if detect_bolded_text(element):
                    element['element-type'] += 'bold;'

                if detect_italicized_text(element):
                    element['element-type'] += 'italic;'

                if detect_underlined_text(element):
                    element['element-type'] += 'underline;'
            else:
                if all([child.name in ['p','span','b','i','ix:nonnumeric','ix:nonfraction','br','a'] for child in children]):
                    element['element-type'] = 'div:'
                    if detect_bolded_text(element):
                        element['element-type'] += 'bold;'

                    if detect_italicized_text(element):
                        element['element-type'] += 'italic;'

                    if detect_underlined_text(element):
                        element['element-type'] += 'underline;'
                else:
                    for child in children:
                        recursive_parser(child)



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


for file in files[0:1]:
    # may want to adjust encoding to utf-8-sig
    with open(file) as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    clean_html(body)
    recursive_parser(body)
    color_parsing(body)
    open_soup(soup)
