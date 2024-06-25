import bs4

from download import download_sec_filing

from html_helper import get_elements_between_two_elements, open_soup, handle_table_of_contents, get_text_between_two_elements

html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/aapl-20200926.htm')

soup = bs4.BeautifulSoup(html, 'html.parser')

from parsers import parse_10k

tree = parse_10k(html)

from xml_helper import print_xml_structure
print_xml_structure(tree)