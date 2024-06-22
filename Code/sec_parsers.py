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

    df = handle_table_of_contents(soup)

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

    # build xml
    root = ET.Element("root")
    current_part = ''
    for idx, row in df.iterrows():
        part = row['part']
        if len(part) > 0:
            if part != current_part:
                current_part = part
                part_element = ET.SubElement(root, part)
            item = ET.SubElement(part_element, row['item'])
            item.text = row['text']
        else:
            item = ET.SubElement(root, row['item'])
            item.text = row['text']
        
    tree = ET.ElementTree(root)
    if visualize:
        open_soup(soup)

    return tree