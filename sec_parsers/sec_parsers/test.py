from download import download_sec_filing
from lxml import etree
from parsers import iterate_element
from xml_helper import open_tree
from style_detection import *


# figure out how to add encoding
# https://www.sec.gov/Archives/edgar/data/1318605/000095017022000796/tsla-20211231.htm encoding issue

sec_html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm')
parser = etree.HTMLParser(encoding='utf-8')
root = etree.fromstring(sec_html, parser)


body = root.find('body')
time = iterate_element(body)
print(time)
open_tree(root)