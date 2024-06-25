import requests

def download_sec_filing(url):
    """Download the SEC filing from the given URL."""
    headers = {
        'User-Agent': 'Sample Company Name AdminContact@<sample company domain>.com'
    }
    sec_response = requests.get(url, headers=headers)

    if sec_response.status_code != 200:
        print(f"Error {sec_response.status_code}: failed to download {url}")
        return None
    
    html = sec_response.text
    return html