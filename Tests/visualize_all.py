from sec_parsers import Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from global_vars import *

import os
import pandas as pd

files = os.listdir(dir_10k)[2:3]
for count,file in enumerate(files):
    with open(dir_10k + file, 'r', encoding='utf-8') as f:
        html = f.read()
        
# check mutability
filing = Parser(html)
filing.parse()
filing.visualize()