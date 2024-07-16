from sec_parsers import set_headers, download_sec_filing
from sec_parsers.experimental_parsers import HTMLParser
from sec_parsers.parsers import setup_html

set_headers('John Smith','example@example.com')

# looks like S-1 filings can be supported with minor tweaks, same for s3
s1_urls = ['https://www.sec.gov/Archives/edgar/data/1713445/000162828024006294/reddits-1q423.htm']
urls_10k = ['https://www.sec.gov/Archives/edgar/data/1318605/000095017022000796/tsla-20211231.htm']

html = download_sec_filing(urls_10k[0])

parser = HTMLParser(html)
