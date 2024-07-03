import requests
import random as rd

# Module to download the SEC filings

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
        print("Please set your own headers using set_headers(name, email)")
        return None
    
    sec_response = requests.get(url, headers=headers)
    
    if sec_response.status_code != 200:
        print(f"Error {sec_response.status_code}: failed to download {url}")
        return None
    
    # important to encode the text as utf-8 as the lxml parser expects it
    html = sec_response.text.encode("utf-8")
    return html

