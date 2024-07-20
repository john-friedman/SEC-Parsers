from sec_parsers import set_headers, download_sec_filing
from sec_parsers import Filing
from sec_parsers.xml_helper import get_all_text
from sec_parsers.style_detection import detect_part
from sec_parsers.experimental_parsers import SEC10KParser
from time import time
from lxml import etree
set_headers('John Smith','example@example.com')

# looks like S-1 filings can be supported with minor tweaks, same for s3
s1_urls = ['https://www.sec.gov/Archives/edgar/data/1713445/000162828024006294/reddits-1q423.htm']
urls_10k = ['https://www.sec.gov/Archives/edgar/data/1318605/000095017022000796/tsla-20211231.htm']
urls_8k =['https://www.sec.gov/Archives/edgar/data/1318605/000095017023038779/tsla-20230804.htm']
html = download_sec_filing(urls_10k[0])

filing = Filing(html)
parser = SEC10KParser()
s= time()
parser.recursive_parse(filing.html)
print(f'Recursive Parsing took {time()-s} seconds')
s = time()
parser.parse_top_level(filing.html)
print(f'Top Level Parsing took {time()-s} seconds')
# s = time()
# parser.relative_parse(filing.html)
# print(f'Relative Parsing took {time()-s} seconds')
s= time()
parser.clean_parse(filing.html)
print(f'Clean Parsing took {time()-s} seconds')

filing.visualize()

s = time()
for elem in filing.html.iter():
    print(elem.tag)
print(f'Getting all text took {time()-s} seconds')