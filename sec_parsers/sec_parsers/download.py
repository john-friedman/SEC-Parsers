import requests
import random as rd

# generate a random number from 1 to 1 million
def random_num():
    return rd.randint(1, 1000000)

# add random number to user agent to avoid being blocked if too many people use package
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
    sec_response = requests.get(url, headers=headers)

    if sec_response.status_code != 200:
        print(f"Error {sec_response.status_code}: failed to download {url}")
        return None
    
    html = sec_response.text
    return html

