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

# remove hidden elements
# may need to tweak
for element in body.select('[style*="display: none"]'):
    element.decompose()
for element in body.select('[style*="display:none"]'):
    element.decompose()

simplified_soup = BeautifulSoup("", 'html.parser')


# mutability is something to keep in mind
def recursive_simplification(element):
    
    # may remove
    if isinstance(element, Tag):
        # if find specific tags, stop else
        if element.name == 'p':
            if element.text.strip() == "":
                element.decompose()
            else:
                new_tag = simplified_soup.new_tag('p')
                new_tag.string = element.text
                # stores if element was parsed
                new_tag['element-type'] = 'parsed'

                if detect_bolded_text(element):
                    add_style(new_tag, 'font-weight: bold;')

                if detect_italicized_text(element):
                    add_style(new_tag,'font-style: italic;')

                simplified_soup.append(new_tag)
                element.decompose()
        elif element.name == 'span':
            if element.text.strip() == "":
                element.decompose()
            else:
                new_tag = simplified_soup.new_tag('p')
                new_tag.string = element.text
                # stores if element was parsed
                new_tag['element-type'] = 'parsed'
                # test if self is bolded or italicized
                if detect_bolded_text(element):
                    add_style(new_tag, 'font-weight: bold;')

                if detect_italicized_text(element):
                    add_style(new_tag,'font-style: italic;')

                simplified_soup.append(new_tag)
                element.decompose()
        # remove breaks
        elif element.name == 'br':
            element.decompose()
        # remove table of contents
        elif element.name == 'a':
            if element.text.strip().lower() == 'table of contents':
                element.decompose()
        # ignore tables for now
        elif element.name in ['table']:
            add_element(element,simplified_soup)
        else:
            # i think we can safely ignore navigable strings
            children = [child for child in element.findChildren(recursive=False) if isinstance(child, Tag)]
            if len(children) > 0:
                for child in children:
                    recursive_simplification(child)
            else:
                add_element(element,simplified_soup)
    

    

recursive_simplification(body)
open_soup(simplified_soup)
#soup = BeautifulSoup(html, 'html.parser')
#open_soup(soup)
