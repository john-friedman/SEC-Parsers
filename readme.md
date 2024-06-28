# Experimental Branch

# TODO tmrw
1. Detailed parsers visualization
2. fix up table stuff (e.g. paragraphs, coloring scheme)
2. add relative parsing
3. naive parse
4. figure out structure for relative parse

# SEC Parsers
Parses non-standardized SEC 10-K filings into well structured xml. Currently can parse about 80% of SEC 10 K filings. XML includes parts, items (such as item1a risk factors), as well as subheadings (e.g. seasonality).

A sample of parsed 10k xmls are available [here](https://www.dropbox.com/scl/fo/np1lpow7r3bissz80ze3o/AKGM8skBrUfEGlSweofAUDU?rlkey=cz1r78jofntjeq4ax2vb2yd0u&e=1&st=mdcwgfcm&dl=0). I would like to upload every parsed 10k xml, but I lack the storage (I need ~50gb, and I have 2gb.) If you can help me with this problem please let me know!

## Functions
* ```parse_10k(html)``` converts a sec filing from non-standardized html into well structured xml
* ```get_table_of_contents(html)``` reads the table of contents from a sec filing html
* ```download_sec_filing(url)``` downloads a sec filing from url using headers
* ```print_xml_structure(tree)``` prints tree structure of parsed html file
* ```get_text_from_node(node)``` gets the text from an xml node

## Quickstart

## Current Issues before merger with main
* add subsection parsing using recursion - old code should help
* add visualization

## On upload to main
* edit stackoverflow questions - I goofed and had a bad package structure. e.g. from sec_parsers.sec_parsers import parse_10k instead of from sec_parsers import parse_10k
* update jupyter notebooks
* add statistics on how many files parsed - (currently looks to be ~75%)
* upload parsed xmls to dropbox and share publicly
* add download for normal branch from pypi, and experimental from pypitest

## Future
* metadata - e.g. <metadata><cik><company_name> etc at base of root. also add tag for document
* more options for parsing, 10Q, etc
* tools to help check if html parsed to xml correctly. (Maybe some side by side flask interface?)
* host parsed 10k xml files (~3000 companies, ~25 years, <50gb) online for download

## Notes:
* Last update to main branch was very WIP with beginner mistakes (never wrote a python package before). I've now settled on a more concrete structure.

## Statistics
Statistics are likely better than they look. Small / weird companies are less likely to parse - make this section generate automatically from tests

Table of Contents Parsing:
* took 12 minutes
* 79.7% parsed
* 14.4% had an issue that can be resolved
* 3% were not parsed has table without links is not supported yet
* remainder unclear


Conversion to xml:
* took 40 minutes
* 93.1% parsed succesfully
* 6.9% had an issue

Total parse rate is 74%.

Last test run on 1039 10-Ks on June 27 2024.

# Subsection Parsing
* read 10 filings to get ideas.
* detect unique test
* need a way to notice if tag is surronded by text e.g. random bolded thing in paragraph
* check if nearest neighbors are unbolded e.g. pART I (caps are bold in this case), assume is subheader
* might just use some combination of detect unique + position (e.g. \n asset management \n)
* actually its more difficult than that, because I need parents and children

## Efficiency
* Code runtime: files parse every ~2 seconds or so. Parsing every 10k filing that is available online would take < 2 days, with multiprocessing, < 4 hours. As such, I will not initially spend effort optimizing runtime. I'll wait until I begin parsing other types of documents where total runtime is much longer to think about optimization.
* Probably will try lxml's html parser. Initial tests suggest its about 2x as fast for this use-case. Also could just use beautifulsoup's lxml parser

## Other useful SEC stuff
* [sec-parser](https://github.com/alphanome-ai/sec-parser) - oops, we have similar names. They were first, my bad. They parse 10-Qs well.
* [edgartools](https://github.com/dgunning/edgartools) - good interface for interacting with SEC's EDGAR system
* [sec-api](https://sec-api.io/). Paid API to search / download SEC filings. Basically, SEC's EDGAR but setup in a much nicer format. I haven't used it since it costs money.
* [Bill McDonald's 10-X Archive](https://sraf.nd.edu/data/stage-one-10-x-parse-data/)