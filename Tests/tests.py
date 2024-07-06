from sec_parsers import *
from global_vars import *

import os
import pandas as pd
from pathlib import Path
columns = ['file','parsed','error']
row_list =[]

# delete files in dir_10k_parsed
dir_10k_parsed_path = Path(dir_10k_parsed)
if dir_10k_parsed_path.exists():
    for file in os.listdir(dir_10k_parsed):
        os.remove(dir_10k_parsed + file)


files = os.listdir(dir_10k)
# randomize the files
import random
random.shuffle(files)

for count,file in enumerate(files):
    if count % 10 == 0:
        df = pd.DataFrame(row_list,columns=columns)
        df.to_csv(test_csv_path)
    try:
        with open(dir_10k + file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # parse the 10-K filing
        parsed_html = parse_10k(html)

        # visualize the parsing
        #visualize_parsing(parsed_html)

        # construct the xml tree
        xml = construct_xml_tree(parsed_html)

        # print the xml tree
        print(get_node_attributes(xml,attribute='desc'))

        print("File: ",file)
        user_input = input("Correct? (y/n)")
        if user_input == 'n':
            raise Exception("User input 'n'")

        # save the xml tree
        save_xml(xml, dir_10k_parsed + file + ".xml")

        # append 
        row = {'file':file,'parsed':True,'error':None}
        row_list.append(row)
        # save
    except Exception as e:
        print(e)
        # append to the dataframe
        row = {'file':file,'parsed':False,'error':str(e)}
        row_list.append(row)
        # save
