from download import download_sec_filing
from lxml import etree
from parsers import iterate_element
from xml_helper import open_tree
from style_detection import *

sec_html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1652044/000165204423000016/goog-20221231.htm')
parser = etree.HTMLParser(encoding='utf-8')
root = etree.fromstring(sec_html, parser)


body = root.find('body')
time = iterate_element(body)
print(time)
open_tree(root)