from bs4 import BeautifulSoup
import re
import pandas as pd
import xml.etree.cElementTree as ET

from helper import open_soup,handle_table_of_contents, generate_pastel_colors,get_text_between_Tags

def parse_10k(html, visualize=True):
    # encoding is tricky with sec files, utf-8-sig seems to work
    # with open(path, encoding='utf-8-sig') as f:
    #     html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    table = handle_table_of_contents(soup)
    

    # parse table of contents
    # if top item has no page number is probably part
    # item rows have item (SEC), item title and link (exact name changes), and page number

    # get all rows
    tables_rows = table.find_all('tr')
    # select rows which have text
    table_rows = [row for row in tables_rows if row.text.strip() != '']

    row_dict_list =[]
    part = ''
    for table_row in table_rows:
        if re.search(r'^part\s+(i|ii|iii|iv)', table_row.text, re.IGNORECASE) is not None:
            part = table_row.text
        else:
            row = {}
            row['part'] = part
            # Parse as item
            for cell in table_row.find_all('td'):
                # item
                if re.search(r'^item', cell.text, re.IGNORECASE) is not None:
                    row['item'] = cell.text
                # link
                elif cell.find('a') is not None:
                    row['link_text'] = cell.find('a').text
                    row['href'] = cell.find('a')['href']

            if len(row) > 1:
                row_dict_list.append(row)

    # convert to dataframe
    df = pd.DataFrame(row_dict_list)

    # drop nan
    # note: in the future, we may want to handle this more gracefully
    df = df.dropna()
    # reset index
    df = df.reset_index(drop=True)


    background_colors = generate_pastel_colors(df.shape[0])

    df['text'] = ''
    for idx, row in df.iterrows():
        if idx < len(df)-1:
            id1 = df.loc[idx, 'href'][1:] 
            id2 = df.loc[idx+1, 'href'][1:]
            elem1 = soup.find(id=id1)
            elem2 = soup.find(id=id2)
            text = get_text_between_Tags(elem1, elem2, background_color=background_colors[idx])
            df.loc[idx, 'text'] = text

    df['item'] = df['href'].str.split('.').str[0].str.replace('#','').str.strip().str.lower()

    # build xml
    root = ET.Element("root")
    for idx, row in df.iterrows():
        item = ET.SubElement(root, row['item'])
        item.text = row['text']
        
    tree = ET.ElementTree(root)
    if visualize:
        open_soup(soup)

    return tree