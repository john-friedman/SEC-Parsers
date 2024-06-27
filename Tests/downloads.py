from edgar import *  #https://github.com/dgunning/edgartools
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import lxml.etree as etree
set_identity("Bob Mccallum bob.mccalum@bob.com")

filings = get_filings(form="10-K", amendments=False)

dir_data = "../Data/"
dir_10k = "../Data/10K/"

# takes ~ 20 minutes to run
for idx,filing in enumerate(filings):
    try:
        company_name = filing.company.replace(' ','_')
        print(f"Downloading {idx}: {company_name}")
        cik = filing.cik
        accession_number = filing.accession_number
        filing_html = filing.html()

        out_path = f"{dir_10k}{company_name}-{str(cik)}-{str(accession_number)}.html"
        with open(out_path, 'w', encoding='utf-8-sig') as f:
            f.write(filing_html)
    except Exception as e:
        print(e)


