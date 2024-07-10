from sec_parsers import Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from global_vars import *

import os
import pandas as pd
from time import time

#file 7 is interesting

#for parsing - ~100% parse without error - this makes sense.
# for xml - 28% error rate - should go way down, with parser fixed.
files = os.listdir(dir_10k)[0:1]
errors = []
for count,file in enumerate(files):
    s = time()
    with open(dir_10k + file, 'r', encoding='utf-8') as f:
        html = f.read()
        
    filing = Parser(html)
    filing.parse()
    filing.visualize()
    filing.to_xml()
    #filing.to_xml()
    #print(filing.get_node_tree_attributes())

    print(f'File {count} took {time()-s} seconds')
