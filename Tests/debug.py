from sec_parsers import Filing, download_sec_filing, set_headers
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing,parse_metadata, detect_filing_type
from sec_parsers.xml_helper import get_elements_between_elements, get_text_between_elements, get_all_text
from global_vars import *
from lxml import etree
import os

from time import time

html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1318605/000095017023033872/tsla-20230630.htm')

filing = Filing(html)

filing.visualize()