from sec_parsers import Filing,download_sec_filing,set_headers
set_headers('My Name','myemail@outlook.com')
url = 'https://www.sec.gov/Archives/edgar/data/1793659/000179365923000010/rsi-20221231.htm'
html = download_sec_filing(url)
sec_filing = Filing(html)
sec_filing.set_filing_type('10-K')
print(sec_filing.filing_type)
sec_filing.parse()
print(sec_filing.get_title_tree())