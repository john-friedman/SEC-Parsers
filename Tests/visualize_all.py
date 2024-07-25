from sec_parsers import Filing,download_sec_filing,set_headers
from global_vars import *
from sec_parsers.xml_helper import get_all_text

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
print(os.listdir(dir_10k_parsed))


total_time = 0
start_dex = 0
files = os.listdir(dir_10k)[0:5]
errors = []
for count,file in enumerate(files):
        try:
            s = time()
            with open(dir_10k + file, 'r', encoding='utf-8') as f:
                html = f.read()
                
            filing = Filing(html)
            filing.parse()
            filing.visualize()
            print(filing.get_title_tree())

            total_time += time()-s
            print(f'File {count+start_dex} took {time()-s} seconds')

            print(f'Average parsing time: {total_time/(count+1)} seconds')
            print(f"total time: {total_time}")
            # filing.save_xml(dir_10k_parsed + file[:-5] + '.xml')
            # filing.save_xml('testa.xml')
        except Exception as e:
            errors.append((file,e))
            print(f'Error in {file}: num_errors = {len(errors)}')
            print(f"count: {count}")
            print(e)
print(f"Error percentage: {len(errors)/len(files)}")
# save errors to text file
with open('errors.txt', 'w') as f:
    for error in errors:
        f.write(str(error) + '\n')
