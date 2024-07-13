from sec_parsers import Filing, download_sec_filing, set_headers
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing,parse_metadata, detect_filing_type
from sec_parsers.xml_helper import get_elements_between_elements, get_text_between_elements, get_all_text
from global_vars import *
from lxml import etree
import os
import random
from time import time

file = 'Alaunos_Therapeutics,_Inc.-1107421-0000950170-24-038868.html'
with open(dir_10k + file, 'r', encoding='utf-8') as f:
    html = f.read()


filing = Filing(html)
recursive_parse(filing.html)
relative_parsing(filing.html)
cleanup_parsing(filing.html)
filing.visualize()