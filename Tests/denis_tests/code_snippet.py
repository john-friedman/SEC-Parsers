from sec_parsers import Parser, download_sec_filing, set_headers

set_headers('Example Name','examplemeail@example.com')
html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/18255/000001825518000024/cato10k2017-jrs.htm')


parser = Parser(html)
parser.parse()

parser.save_xml('cato10k2017-jrs.xml')
parser.save_csv('cato10k2017-jrs.csv')

parser.visualize()
