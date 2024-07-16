from sec_parsers import Filing,download_sec_filing,set_headers
from sec_parsers.parsers import recursive_parse, relative_parsing, cleanup_parsing
from global_vars import *

import os
import pandas as pd
from time import time

set_headers('John Smith','example@example.com')
# delete everything in dir_10k_parsed
file_list = os.listdir(dir_10k_parsed)
for file in file_list:
    file_path = os.path.join(dir_10k_parsed, file)
    if os.path.isfile(file_path):
        os.remove(file_path)


total_time = 0
start_dex = 100
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


            print(filing.get_title_tree())

            print(f'File {count+start_dex} took {time()-s} seconds')
            total_time += time()-s
            #print(f'Average parsing time: {total_time/(count+1)} seconds')
            filing.save_xml(dir_10k_parsed + file[:-5] + '.xml')
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
