from download import download_sec_filing
from lxml import etree
from parsers import recursive_parse
from xml_helper import open_tree
from style_detection import *
import os
from time import time


dir_10k = "../../Data/10K"
files = os.listdir(dir_10k)
files = [dir_10k + "/" + file for file in files]
for file in files[0:1]:
    print(file)
    with open(file, 'r',encoding='utf-8') as f:
        sec_html = f.read()

parser = etree.HTMLParser(encoding='utf-8',remove_comments=True)
s1 = time()
root = etree.fromstring(sec_html, parser)
recursive_parse(root)
e1 = time()
print(e1-s1)
open_tree(root)