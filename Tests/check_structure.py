from sec_parsers import *
from global_vars import *

import os
import pandas as pd

files = os.listdir(dir_10k)
for count,file in enumerate(files):
    try:
        with open(dir_10k + file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # parse the 10-K filing
        parsed_html = parse_10k(html)

        # construct the xml tree
        xml = construct_xml_tree(parsed_html)

        # print the xml tree
        print(get_node_attributes(xml,attribute='desc'))

        input("Press Enter to continue...")
    except Exception as e:
        print(e)