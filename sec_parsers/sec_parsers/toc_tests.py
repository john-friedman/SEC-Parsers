# tests for checking if the table of contents was read correctly
import bs4
import pandas as pd
import re
from download import download_sec_filing
import os
from html_helper import get_table_of_contents, open_soup, detect_table_of_contents

# initial results out of 58. 41 parsed, 13 errors, 4 skipped (due to no table of contents)
# looks like we can fix 9 or so of the errors. so 50/58 parsed or 86% parsed

def view_errors():
    parsing_df = pd.read_csv("parsing_tests.csv")
    for idx, row in parsing_df[parsing_df.toc_parsed == 'error'].iterrows():
        with open(row['file'], 'r', encoding='utf-8-sig') as f:
            html = f.read()
        
        soup = bs4.BeautifulSoup(html, 'html.parser')
        open_soup(soup)

dir_10k = "../../Data/10K/"
out_path = "parsing_tests.csv"
def generate_tests_df(dir_10k,out_path):
    files = os.listdir(dir_10k)
    files = [dir_10k + file for file in files]
    df = pd.DataFrame(files, columns=['file'])
    df['toc_parsed'] = ''
    df['html_parsed'] = ''
    df.to_csv(out_path, index=False)

def check_toc_parsing(toc_dict):
    # Extracting the relevant information and creating a DataFrame
    records = []
    for part in toc_dict['parts']:
        for item in part['items']:
            records.append({
                'part': part['name'],
                'item': item['name'],
                'desc': item['desc'],
                # 'item_href': item['href'],
                # 'part_href': part['href'],
            })

    df = pd.DataFrame(records)
    return df

parsing_df = pd.read_csv(out_path)
for idx, row in parsing_df[parsing_df.toc_parsed.isna()].iterrows():
    try:
        file = row['file']
        print(f"{idx}: {file}")
        with open(file, 'r', encoding='utf-8-sig') as f:
            html = f.read()

        soup = bs4.BeautifulSoup(html, 'html.parser')

        toc_dict = get_table_of_contents(soup)
        df = check_toc_parsing(toc_dict)
        print(df)
        
        confirmation = input("Does this look correct? (press y to confirm)")

        if confirmation == 'y':  # Check for an empty string (Enter key press)
            print('Confirmed!')
            parsing_df.loc[idx, 'toc_parsed'] = 'parsed'
        else:
            open_soup(soup)
            if input("skip by pressing s. otherwise debug") == 's':
                parsing_df.loc[idx, 'toc_parsed'] = 'skipped'
            else:
                break

        parsing_df.to_csv(out_path, index=False)
            
    except Exception as e:
        print(e)
        parsing_df.loc[idx, 'toc_parsed'] = 'error'
        parsing_df.to_csv(out_path, index=False)    
