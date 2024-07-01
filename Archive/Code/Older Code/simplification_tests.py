from bs4 import BeautifulSoup, NavigableString, Tag
from helper import open_soup, add_class, add_style
import re

with open('test.html',encoding='utf-8-sig') as f:
    html_string = f.read()


# before converting to soup
# apply some preprocessing to clean up non standard characters
html_string = re.sub(r'([\s+]|(\&nbsp\(;)*)){1,}', ' ', html_string)


soup = BeautifulSoup(html_string, 'html.parser')
body = soup.body

for child in body.children:
    print(child)

def standardize_italics(body):
    for tag in body.find_all('i'):
        string = tag.string
        parent = tag.parent
        if parent.string == string:
            add_style(parent, 'font-style: italic;')
            tag.decompose()
            parent.string = string

def standardize_bold(body):
    for tag in body.find_all('b'):
        string = tag.string
        parent = tag.parent
        if parent.string == string:
            add_style(parent, 'font-weight: bold;')
            tag.decompose()
            parent.string = string






    
    
standardize_italics(body)
standardize_bold(body)
open_soup(soup)