from bs4 import BeautifulSoup
import os
from html_parser import recursive_parser, color_parsing
from helper import clean_html, open_soup
from xml_builder import xml_builder

# code to test:
# load all 10-k files
dir_10k = "../Data/10K"
files = []
for file in os.listdir(dir_10k):
    files.append(f"{dir_10k}/{file}")


for file in files[1:2]:
    # may want to adjust encoding to utf-8-sig
    with open(file, encoding='utf-8-sig') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    # remove non breaking spaces
    #soup = BeautifulSoup(soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' ')),'html.parser')

    body = soup.find('body')

    clean_html(body)
    recursive_parser(body)
    color_parsing(body)
    open_soup(soup)

    # with open('test.html', encoding='utf-8-sig') as f:
    #     html = f.read()
    # element = BeautifulSoup(html).find('table')
