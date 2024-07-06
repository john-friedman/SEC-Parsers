from sec_parsers import *
from global_vars import *

import os
import pandas as pd
from pathlib import Path
from lxml import etree

files = os.listdir(dir_10k)
file = dir_10k + '/' + files[0]

with open(file, 'r', encoding='utf-8') as f:
    html = f.read()

# parse the 10-K filing
parsed_html = parse_10k(html)

# visualize the parsing
#visualize_parsing(parsed_html)

# construct the xml tree
xml = construct_xml_tree(parsed_html)

# print the xml tree
print(get_node_attributes(xml,attribute='desc'))