import pandas as pd
from sec_parsers import parse_10k, open_soup,get_table_of_contents
from bs4 import BeautifulSoup
import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag
import random
import pandas as pd

# OK, so issue is some don't have parts in table of contents.
# Note: a lot of these + efficiency can be improved by ignoring table of contents and doing smart relative detection
# which we'll implement using lessons from first detailed parser pass

df = pd.read_csv("parsing_tests.csv")

files = df[df.html_parsed!='true'].file.tolist()
errors = []
for idx, file in enumerate(files):
    try:
        with open(file, 'r',encoding='utf-8-sig') as f:
            html = f.read()

        tree = parse_10k(html)
    except Exception as e:
        errors.append((file, e))


        
#count types of errors. To tackle first: "'NoneType' object has no attribute 'group'",
#"string indices must be integers, not 'str'",
#"'NoneType' object has no attribute 'next'",
error_types = {}
for error in errors:
    error_type = error[1].args
    if error_type in error_types:
        error_types[error_type] += 1
    else:
        error_types[error_type] = 1

#save errors to file
with open('errors.txt', 'w') as f:
    for error in errors:
        f.write(f'{error[0]}: {error[1]}\n')

from sec_parsers.html_helper import detect_table_of_contents

file = '../Data/10K/Aimfinity_Investment_Corp._I-1903464-0001213900-24-032604.html'
with open(file, 'r',encoding='utf-8-sig') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

tree = parse_10k(html)


soup = BeautifulSoup(html, 'html.parser')
open_soup(soup)