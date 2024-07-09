from sec_parsers import download_sec_filing, set_headers, Parser
import pandas as pd


set_headers("John Doe","Johndoe@anemail.com")
html = download_sec_filing("https://www.sec.gov/Archives/edgar/data/1318605/000162828024017503/tsla-20240331.htm")

parser = Parser(html)
parser.parse()
#parser.visualize()
elem1 = parser.find_nodes_by_desc('Energy Generation and Storage Segment')[0]

print(parser.get_node_text(elem1))