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


path = files[0]

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


# mutability is something to keep in mind
# changing approach to mark in attributes
def recursive_simplification(element):
    
    # may remove
    if isinstance(element, Tag):
        # if find specific tags, stop else
        if element.name == 'p':
            if element.text.strip() == "":
                element['element-type'] = 'empty'
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
                element['element-type'] = 'empty'
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
                element['element-type'] = 'toc-link'
                return
        # ignore tables for now
        elif element.name in ['table']:
                element['element-type'] = 'table'
                return
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
