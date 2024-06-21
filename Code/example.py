import os
from sec_parsers import parse_10k
from edgar import *
from bs4 import BeautifulSoup

set_identity("Michael Mccallum mike.mccalum@indigo.com")
filings = Company("AMZN").get_filings(form="10-K").latest(1)
html = filings.html()

#path = "../Data/10K/1961_0001264931-24-000014.html"
xml = parse_10k(html, visualize=True)

# save xml to file
xml.write('parsed_10k.xml')

from helper import handle_table_of_contents

table = handle_table_of_contents(xml)