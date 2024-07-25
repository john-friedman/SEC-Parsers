from sec_parsers import Filing,download_sec_filing,set_headers
set_headers('My Name','myemail@outlook.com')
urls = ['https://www.sec.gov/Archives/edgar/data/350868/000035086824000016/iti-20240331.htm','https://www.sec.gov/Archives/edgar/data/88948/000143774924020198/senea20240331_10k.htm']
html = download_sec_filing(urls[1])
sec_filing = Filing (html)
sec_filing.parse()

item1c = sec_filing.find_section_from_title('Item 1C')
nested_subsections = sec_filing.get_nested_subsections_from_section(item1c)
print([item.attrib['title'] for item in nested_subsections])
print(sec_filing.get_title_tree())