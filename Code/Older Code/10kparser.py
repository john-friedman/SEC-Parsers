from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import numpy as np
import lxml.etree as etree
import os
import re
import webbrowser
from helper import *


dir_10k = "../Data/10K"
files = os.listdir(dir_10k)
file = files[0]
path  = dir_10k + "/" + file
path = "../Data/10K/1961_0001264931-24-000014.html"
with open(path) as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')

# maybe try to parse 1 type of file first to learn how to do other unstructured
# parser 1

# decomposing tables for now #TODO
for table in soup.find_all("table"):
    table.decompose()
element_list = soup.find_all(['p','span'])

# header can use to check if parsing correct
# todo: check marks     

current_index = 0
current_index, header_string  = extract_text_before_anchor(element_list,current_index,"For the transition period from")
current_index, commission_file_number_string = extract_text_before_anchor(element_list,current_index,"Commission File Number")
current_index, exact_name_of_registrant_string = extract_text_before_anchor(element_list,current_index,"Exact name of registrant as specified in its charter")

# we're going to skip now to table of contents
current_index, _ = find_anchor(element_list,current_index,"Table of Contents")

# how to deal with tables...

# skip to part 1
current_index, part1_element = find_anchor(element_list,current_index,"Part I")

# start constructing tree
# change to xml eventually
# using text for now
from lxml import etree
part1 = etree.Element(re.sub(r"\s+", "", part1_element.text))

for idx,element in enumerate(element_list[current_index+1:]):
    text = element.text.strip()
    if text == "":
        continue
    if not is_paragraph(element):
        part1.append(etree.Element(re.sub(r"\s+", "", text)))

etree.tostring(part1)