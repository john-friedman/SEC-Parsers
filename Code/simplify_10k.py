from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import re
from helper import open_soup, add_style, add_element

# convert the 10-k to a simplier html
# build the tree

#path = "../Data/10K/1961_0001264931-24-000014.html"
path = "../Data/10K/6845_0000006845-24-000088.html"

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
                new_tag['element-parsed'] = 'true'
                # children
                descendant_tags = [tag for tag in element.findChildren(recursive=True) if isinstance(tag, Tag)]
                if 'b' in [tag.name for tag in descendant_tags]:
                    add_style(new_tag, 'font-weight: bold;')
                
                if 'i' in [tag.name for tag in descendant_tags]:
                    add_style(new_tag,'font-style: italic;')

                simplified_soup.append(new_tag)
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
    
    
# worked ok
# for child in children:
#     if isinstance(child, Tag):
#         # due to mutability, this looks like it delets from soup
#         if child.name in ['p']:
#             if child.text.strip() == "":
#                 child.decompose()
#             else:
#                 new_tag = simplified_soup.new_tag('p')
#                 new_tag.string = child.text
#                 # children
#                 descendant_tags = [tag for tag in child.findChildren(recursive=True) if isinstance(tag, Tag)]
#                 if 'b' in [tag.name for tag in descendant_tags]:
#                     add_style(new_tag, 'font-weight: bold;')
                
#                 if 'i' in [tag.name for tag in descendant_tags]:
#                     add_style(new_tag,'font-style: italic;')

#                 simplified_soup.append(new_tag)
#                 child.decompose()
#         # ignore tables for now
#         elif child.name in ['table']:
#             child.decompose()
#         else:
#             simplified_soup.append(child)
    

recursive_simplification(body)
open_soup(simplified_soup)
soup = BeautifulSoup(html, 'html.parser')
open_soup(soup)
