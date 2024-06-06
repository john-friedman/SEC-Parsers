from bs4 import BeautifulSoup
import os
from html_parser import recursive_parser
from helper import clean_html, open_soup
from xml_builder import xml_builder, color_parsing

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
