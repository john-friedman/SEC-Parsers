from sec_parsers import Filing, download_sec_filing, set_headers
from sec_parsers.xml_helper import get_all_text
from sec_parsers.cleaning import part_pattern

def print_first_n_lines(text, n):
    lines = text.split('\n')
    for line in lines[:n]:
        print(line)

set_headers("John Test",'johntest@example.com')
html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1318605/000095017023033872/tsla-20230630.htm')

filing = Filing(html)
filing.parse()

parts_elements = filing.html.xpath("//*[@parsing_type='part;']")
first_part_element = [element for element in parts_elements if part_pattern.match(get_all_text(element).strip().lower())][0]
part_pattern.match(get_all_text(parts_elements[1]).strip().lower())