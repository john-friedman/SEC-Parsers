from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
import numpy as np
import lxml.etree as etree
import os
import re
import webbrowser
import tempfile
import webbrowser

from helper import open_soup, detect_unique_text

# works well

# element.contents - might even justify rewrite



dir_10k = "../Data/10K"
files = os.listdir(dir_10k)

for file in files[0:5]:
    path  = dir_10k + "/" + file
    with open(path) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # cleaning

    # remove hidden elements
    # may need to tweak
    for element in soup.select('[style*="display: none"]'):
        element.decompose()

    # decomposing tables for now #TODO
    # yay! have to bring back tables now lol
    for table in soup.find_all("table"):
        table.decompose()

    # replace elements without text as space

    # replace all empty elements line breaks?

    body = soup.find('body')


    clean_element(body)
    mark_unique_text(body)
    marked_elements = body.select('[style*="background-color:SandyBrown;"]')
    for marked_element in marked_elements:
        if marked_element.parent:
            combine_elements(marked_element.parent)

    open_soup(soup)
    #webbrowser.open('file://' +os.path.abspath(path) )






