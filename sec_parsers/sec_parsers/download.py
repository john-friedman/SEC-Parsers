import requests
import random as rd
import warnings
import re

# WARNING: This code will eventually be removed from SEC Parsers when SEC Downloaders is implemented.

def extract_cik_and_accession(url):
    # Regular expression pattern to match CIK and accession number
    pattern = r"/data/(\d+)/(\d+)/"
    
    # Search for the pattern in the URL
    match = re.search(pattern, url)
    
    if match:
        cik = match.group(1)
        accession_number = match.group(2)
        return cik, accession_number
    else:
        return None, None


# Module to download the SEC filings
#TODO I'm happy with this file so far.

def random_num():
    return rd.randint(1, 1000000)


headers = {
    'User-Agent': f'Sample Company Name {str(random_num)} AdminContact@<sample company domain>.com'
}

def set_headers(name, email):
    """Set the headers for the requests."""
    global headers
    headers['User-Agent'] = f'{name} {email}'

def download_sec_filing(url):
    """Download the SEC filing from the given URL."""
    global headers

    # nudge to set your own headers
    if 'Sample Company Name' in headers['User-Agent']:
        warnings.warn("Warning: Please set your own headers using set_headers(name, email).")

    sec_response = requests.get(url, headers=headers)
    
    if sec_response.status_code != 200:
        print(f"Error {sec_response.status_code}: failed to download {url}")
        return None
    
    # important to encode the text as utf-8 as the lxml parser expects it
    html = sec_response.text.encode("utf-8").decode("utf-8")
    return html
