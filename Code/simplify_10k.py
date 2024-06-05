from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import re
import os

from helper import open_soup, add_style, add_element, detect_bolded_text, detect_italicized_text

# convert the 10-k to a simplier html
# build the tree

# load all 10-k files
dir_10k = "../Data/10K"
files = []
for file in os.listdir(dir_10k):
    files.append(f"{dir_10k}/{file}")


path = files[3]

# may want to adjust encuding to utf-8-sig
with open(path) as f:
    html = f.read()

# dont know how to deal with non breaking space
# apply some preprocessing to clean up non standard characters
# html = re.sub('[^\S\n]{1,}', ' ', html)
# html = re.sub('\u00A0',' ', html)


soup = BeautifulSoup(html, 'html.parser')
body = soup.find('body')

# reminder to look for element-type, as we will be using that attribute
#TODO

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


simplified_soup = BeautifulSoup("", 'html.parser')


def recursive_simplification(element):
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
                return
        # remove breaks
        elif element.name == 'br':
            element['element-type'] = 'line-break'
            return
        # remove table of contents
        elif element.name == 'a':
            if element.text.strip().lower() == 'table of contents':
                element['element-type'] = 'a:toc-link'
                return
        # ignore tables for now
        elif element.name in ['table']:
                element['element-type'] = 'table'
                return
        # parses div. THIS IS HARD
        elif element.name == 'div':
            children = [child for child in element.findChildren(recursive=False) if isinstance(child, Tag)]
            if len(children) > 0:
                if all(child.tag in ['b','i'] for child in children):
                    element['element-type'] = 'div:'
                    if detect_bolded_text(element):
                        element['element-type'] += 'bold;'

                    if detect_italicized_text(element):
                        element['element-type'] += 'italic;'
        else:
            # i think we can safely ignore navigable strings
            children = [child for child in element.findChildren(recursive=False) if isinstance(child, Tag)]
            if len(children) > 0:
                for child in children:
                    recursive_simplification(child)
            else:
                return
    
# color
def color_parsing(soup):
    # https://www.htmlcodes.ws/color/html-color-code-generator.cfm?colorName=PowderBlue
    
    # browns
    # empty colors

    # reds
    # skipping colors

    # use oranges
    # header colors

    # use lavenders
    # text colors

    # change to a list of colors
    color_list = ['Cornsilk','BlanchedAlmond','Bisque','NavajoWhite','Wheat','BurlyWood','Tan','RosyBrown','SandyBrown','Goldenrod','DarkGoldenrod','Peru','Chocolate','SaddleBrown','Sienna','Brown','Maroon']
    # hard code colors
    # need to tweak
    color_dict = {}
    for element in soup.find_all(attrs={'element-type': True}):
        element_type = element['element-type']
        if element_type in color_dict.keys():
            add_style(element, f"background-color:{color_dict[element_type]};")
        else:
            color = color_list.pop(0)
            color_dict[element_type] = color
            add_style(element, f"background-color:{color};")
    

recursive_simplification(body)
color_parsing(body)
open_soup(soup)
