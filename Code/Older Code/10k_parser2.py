from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import numpy as np
import lxml.etree as etree
import os
import re



# todo page breaks (ignore for now)
# generate tree
# start at root
# PART I, etc
# check multiple filings

#elem = soup(text='provided that')[0].parent

def is_valid_url(string):
    if re.search(r"^(http|www).*(\.com|\.org|\.gov)$", string):
        return True
    else:
        return False




dir_10k = "../Data/10K"
files = os.listdir(dir_10k)
file = files[0]
for file in files:
    path  = dir_10k + "/" + file
    #path = "../Data/10K/1001171_0001140361-24-026827.html"
    with open(path) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    # decomposing tables for now #TODO
    for table in soup.find_all("table"):
        table.decompose()

    # decomposing table of contents links for now
    for a in soup.find_all("a"):
        if "table of contents" in a.text.lower():
            a.decompose()

        
    TAGS_TO_APPEND = ["div", "p", "h1","b","i","u","strong","em","span"]


    # find lowest level text
    # start at 1 to skip xbrls
    empty_tags = []

    #triggers at part 1 to ignore boring stuff
    for element in soup.findAll(TAGS_TO_APPEND)[1:]:
        # may be issue here
        tags = [element for x in element.contents if isinstance(x, NavigableString)]

        for tag in tags:        
            if tag.text.strip() == "":
                empty_tags.append(tag)
                continue

            if detect_unique_text(tag):
                tag['style'] ="background-color:SandyBrown;"
            else:
                tag['style'] ="background-color:powderblue;"
    #clear empty tags
    for tag in empty_tags:
        tag.decompose()
    



    html = str(soup)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)
    webbrowser.open('file://' +os.path.abspath(path) )

    input("Press Enter to continue...")
