from download import download_sec_filing
from lxml import etree
from parsers import recursive_parse, visualize_tree
from style_detection import *
import os
from time import time


dir_10k = "../../Data/10K"
files = os.listdir(dir_10k)
files = [dir_10k + "/" + file for file in files]

parser = etree.HTMLParser(encoding='utf-8',remove_comments=True)

for file in files[12:15]:
    print(file)
    with open(file, 'r',encoding='utf-8') as f:
        sec_html = f.read()

    s1 = time()
    root = etree.fromstring(sec_html, parser)
    recursive_parse(root)
    e1 = time()
    print(e1-s1)
    visualize_tree(root)


element = root.xpath('//table')[3]
