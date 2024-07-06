from sec_parsers import *
from global_vars import *

import os
import pandas as pd

files = os.listdir(dir_10k)
for count,file in enumerate(files):
    with open(dir_10k + file, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # parse the 10-K filing
    parsed_html = parse_10k(html)

    # visualize the parsing
    visualize_parsing(parsed_html)
    #input("Press Enter to continue...")
    if ((count % 2 == 0) and (count != 0)):
        break