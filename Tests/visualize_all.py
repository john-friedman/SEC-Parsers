from sec_parsers import Filing
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from global_vars import *

import os
import pandas as pd
from time import time

# American_Strategic_Investment_Co.-1595527-0001595527-24-000006.html - has no signature so does not parse. this will fix automatically\
# when we update xml construct tree
# good example of big page bloc, 'ATLANTIC_AMERICAN_CORP-8177-0001140361-24-016971.html' need to fix this

# I think we updatte the xml construct, and then parse rate will get to 99% or so, but then we will need
# to focus on fixing tree issues (detect long headers, etc) as they are likely to be wrong



total_time = 0
start_dex = 0
files = os.listdir(dir_10k)[0:1]
errors = []
for count,file in enumerate(files):
        try:
            s = time()
            with open(dir_10k + file, 'r', encoding='utf-8') as f:
                html = f.read()
                
            filing = Filing(html)
            # recursive_parse(filing.html)
            # relative_parsing(filing.html)
            # cleanup_parsing(filing.html)
            # filing.visualize()  
            filing.parse()


            #print(filing.get_title_tree())

            #print(f'File {count+start_dex} took {time()-s} seconds')
            total_time += time()-s
            #print(f'Average parsing time: {total_time/(count+1)} seconds')
        except Exception as e:
            errors.append((file,e))
            print(f'Error in {file}: num_errors = {len(errors)}')
            print(f"count: {count}")
            print(e)
print(len(errors) / len(files))
# save errors to text file
with open('errors.txt', 'w') as f:
    for error in errors:
        f.write(str(error) + '\n')
