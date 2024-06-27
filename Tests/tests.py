import bs4
import pandas as pd
import os
from sec_parsers import get_table_of_contents, open_soup
from sec_parsers import parse_10k
import numpy as np
from time import time

def view_errors():
    parsing_df = pd.read_csv("parsing_tests.csv")
    for idx, row in parsing_df[parsing_df.toc_parsed == 'error'].iterrows():
        with open(row['file'], 'r', encoding='utf-8-sig') as f:
            html = f.read()
        
        soup = bs4.BeautifulSoup(html, 'html.parser')
        open_soup(soup)


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

def run_toc_tests(dir_10k,out_path,new=False):
    if new:
        generate_tests_df(dir_10k,out_path)

    parsing_df = pd.read_csv(out_path)
    for idx, row in parsing_df[parsing_df.toc_parsed.isna()].iterrows():
        try:
            file = row['file']
            with open(file, 'r', encoding='utf-8-sig') as f:
                html = f.read()

            soup = bs4.BeautifulSoup(html, 'html.parser')

            toc_dict = get_table_of_contents(soup)
            df = check_toc_parsing(toc_dict)
            #print(df)

            parsing_df.loc[idx, 'toc_parsed'] = 'true'
            parsing_df.to_csv(out_path, index=False)
                
        except Exception as e:
            print(f"{idx}: {file}")
            print(e)
            parsing_df.loc[idx, 'toc_parsed'] = str(e)
            
            parsing_df.to_csv(out_path, index=False)    

def run_parsing_tests(out_path,new=False):
    df = pd.read_csv(out_path)
    if new:
        df['html_parsed'] = np.nan

    for idx, row in df[((df.html_parsed.isna()) & (df.toc_parsed=='true'))].iterrows():
        try:
            file = row['file']
            with open(file, 'r', encoding='utf-8-sig') as f:
                html = f.read()

            soup = bs4.BeautifulSoup(html, 'html.parser')
            tree = parse_10k(html)
            df.loc[idx, 'html_parsed'] = 'true'
            df.to_csv(out_path, index=False)
        except Exception as e:
            print(f"{idx}: {file}")
            print(e)
            df.loc[idx, 'html_parsed'] = str(e)
            df.to_csv(out_path, index=False)
