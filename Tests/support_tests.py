from sec_parsers import set_headers, download_sec_filing
from sec_parsers import Filing
from sec_parsers import SEC_10K_Parser
set_headers('John Smith','example@example.com')

# looks like S-1 filings can be supported with minor tweaks, same for s3
s1_urls = ['https://www.sec.gov/Archives/edgar/data/1713445/000162828024006294/reddits-1q423.htm','https://www.sec.gov/Archives/edgar/data/1640147/000162828020013010/snowflakes-1.htm']
urls_10k = ['https://www.sec.gov/Archives/edgar/data/1318605/000095017022000796/tsla-20211231.htm']
urls_8k =['https://www.sec.gov/Archives/edgar/data/1318605/000095017023038779/tsla-20230804.htm']
urls_20f = ['https://www.sec.gov/Archives/edgar/data/1543415/000119312512420180/d421925d20f.htm']
html = download_sec_filing(urls_10k[0])

filing = Filing(html)
filing.set_filing_type('10-K')

filing.parse()
print(filing.get_title_tree())
