from sec_parsers import Parser
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from global_vars import *

import os
import pandas as pd
from time import time

#file 7 is interesting

#for parsing - ~100% parse without error - this makes sense.
# for xml - 28% error rate - should go way down, with parser fixed.

# 7-8 is weird check earlier to see if introduced wierd. seems fine. let's see if parsing issues remived
#35
total_time = 0
start_dex = 0
files = os.listdir(dir_10k)[start_dex:]
errors = []
for count,file in enumerate(files):
        try:
            s = time()
            with open(dir_10k + file, 'r', encoding='utf-8') as f:
                html = f.read()
                
            filing = Parser(html)
            # recursive_parse(filing.html)
            # relative_parsing(filing.html)
            # cleanup_parsing(filing.html)
            # filing.visualize()  
            filing.parse()


            #print(filing.get_title_tree())

            print(f'File {count+start_dex} took {time()-s} seconds')
            total_time += time()-s
        except Exception as e:
            errors.append((file,e))
            print(f'Error in {file}: num_errors = {len(errors)}')
            print(e)

print(len(errors) / len(files))
print(f'Total time: {total_time} seconds')