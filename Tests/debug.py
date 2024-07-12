from sec_parsers import Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from sec_parsers.xml_helper import get_elements_between_elements, get_text_between_elements
from global_vars import *
from lxml import etree
import os

from time import time

files = os.listdir(dir_10k)[0:1]
for count,file in enumerate(files):
    with open(dir_10k + file, 'r', encoding='utf-8') as f:
        html = f.read()

    filing = Parser(html)

html = filing.html

elem1 = html.getchildren()[1].getchildren()[-100]

print(get_text_between_elements(html,start_element=elem1))