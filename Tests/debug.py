from sec_parsers import Filing
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing,parse_metadata, detect_filing_type
from sec_parsers.xml_helper import get_elements_between_elements, get_text_between_elements, get_all_text
from global_vars import *
from lxml import etree
import os

from time import time

files = os.listdir(dir_10k)[0:1]
for count,file in enumerate(files):
    with open(dir_10k + file, 'r', encoding='utf-8') as f:
        html = f.read()

    filing = Filing(html)
    filing.parse()
