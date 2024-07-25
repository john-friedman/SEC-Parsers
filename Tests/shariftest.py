from sec_parsers import Filing,download_sec_filing,set_headers
set_headers('John Smith','johnsmoth@example.com')
url = 'https://www.sec.gov/Archives/edgar/data/1015383/000149315224023731/form10-k.htm'
html = download_sec_filing(url)
sec_filing = Filing (html)
sec_filing.parse()
item1c = sec_filing.find_section_from_title('Item 1C')
item1c_text = sec_filing.get_text_from_section(item1c, include_title=True)

sec_filing.get_subsections_from_section(item1c)

print(sec_filing.get_title_tree())
#sec_filing.visualize()