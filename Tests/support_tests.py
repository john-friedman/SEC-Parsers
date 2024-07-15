from sec_parsers import Filing, set_headers, download_sec_filing

set_headers('John Smith','example@example.com')

# looks like S-1 filings can be supported with minor tweaks, same for s3
s1_urls = ['https://www.sec.gov/Archives/edgar/data/1713445/000162828024006294/reddits-1q423.htm']

html = download_sec_filing(urls[0])
filing = Filing(html)
filing.parse()
print(filing.get_title_tree())
filing.visualize()