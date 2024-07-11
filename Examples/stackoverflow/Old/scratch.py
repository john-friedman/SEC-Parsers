#https://stackoverflow.com/questions/31503698/extracting-a-part-of-10k-annual-statement-with-regular-expressions
from sec_parsers import download_sec_filing, parse_10k, construct_xml_tree, get_node_text, set_headers, get_node_attributes, visualize_parsing

# download filing
set_headers("John Doe","johndoe@2mail.com")
html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/867665/000086766513000012/axas12311210k.htm')

# parse filing
parsed_html = parse_10k(html)

 #check parsing is correct
visualize_parsing(parsed_html)