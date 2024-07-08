from sec_parsers import download_sec_filing, parse_10k, construct_xml_tree, get_node_attributes, get_node_text, xml_to_csv, set_headers
import pandas as pd


set_headers("John Doe","Johndoe@anemail.com")
html = download_sec_filing("https://www.sec.gov/Archives/edgar/data/1318605/000162828024017503/tsla-20240331.htm")

parsed_html = parse_10k(html)
xml = construct_xml_tree(parsed_html)
print(get_node_attributes(xml,attribute='desc'))