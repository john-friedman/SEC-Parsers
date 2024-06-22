import os
from sec_parsers import parse_10k
from edgar import *
from bs4 import BeautifulSoup

set_identity("Michael Mccallum mike.mccalum@indigo.com")
filings = Company("TSLA").get_filings(form="10-K").latest(1)
html = filings.html()

path = "../Data/10K/1961_0001264931-24-000014.html"
xml = parse_10k(html, visualize=True)

# save xml to file
xml.write('tsla_parsed_10k.xml')

# import pandas as pd
from helper import handle_table_of_contents
soup = BeautifulSoup(html, 'html.parser')
df = handle_table_of_contents(soup)