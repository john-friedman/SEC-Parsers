from helper import extract_text, print_xml_structure, generate_pastel_colors, open_soup, handle_table_of_contents, get_text_between_Tags, detect_table_of_contents
from bs4 import BeautifulSoup
import pandas as pd
from xml.etree import ElementTree as ET
import re
urls = [
    "https://www.sec.gov/Archives/edgar/data/1350653/000156459018005156/atec-10k_20171231.htm", #worked
    "https://www.sec.gov/Archives/edgar/data/1591890/000149315218003887/form10-k.htm", # worked
    "https://www.sec.gov/Archives/edgar/data/750574/000119312518080325/d472492d10k.htm", # worked
    "https://www.sec.gov/Archives/edgar/data/773840/000093041318000292/c89913_10k.htm", # no
    "https://www.sec.gov/Archives/edgar/data/12927/000001292718000007/a201712dec3110k.htm" # worked
]

# modify for all urls
# get a 10-K filing
import requests
headers = {
    'User-Agent': 'Sample Company Name AdminContact@<sample company domain>.com'
}

html_list = []
for url in urls[3:4]:
    sec_response = requests.get(url, headers=headers)
    html = sec_response.text
    html_list.append(html)

soup = BeautifulSoup(html, 'html.parser')
df = handle_table_of_contents(soup)
print(df)