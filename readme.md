## SEC Parsers
![PyPI - Downloads](https://img.shields.io/pypi/dm/sec-parsers)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fhttps%2F%2Fgithub.com%2Fjohn-friedman%2FSEC-Parsers&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![GitHub](https://img.shields.io/github/stars/john-friedman/sec-parsers)

Parses non-standardized SEC filings into structured xml. Use cases include LLMs, NLP, and textual analysis. Average parse-time for a 100 page document is 0.4 seconds. To view interactive examples click [here](https://jgfriedman99.pythonanywhere.com/parsing).

Supported filing types are 10-K, 10-Q, 8-K, S-1, 20-F. More will be added soon, or you can write your own! [How to write a Custom Parser in 5 minutes](https://medium.com/@jgfriedman99/how-to-write-a-custom-sec-parser-in-5-minutes-5c7a8d5d81b0)

<em>Update:</em> I figured out how to parse almost all SEC filing types at a speed of about 40,000 pages per second on a standard laptop. I am not releasing this parser, because I am currently using it as collateral to raise funding for compute and data hosting as I've reached the end of what I can do with one laptop. The website for the startup is [here](https://jgfriedman99.pythonanywhere.com/) if you want to check it out. Ignore most of the text, that's placeholders for VC. 

TLDR: Package still being supported, but I'll be updating it less and focusing on UI. There will also be a website with a database that is more accessible to non-programmers soon, with a nice free tier.

<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_visualizationv3.png">
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_tree_v4.png" width="500">
</div>

### Installation
```
pip install sec-parsers # base package
pip install sec-parsers['all'] # installs all extras
pip install sec-parsers['downloaders'] # installs downloaders extras
pip install sec-parsers['visualizers'] # installs visualizers extras
```
Links: [SEC Downloaders](https://github.com/john-friedman/SEC-Downloaders), [SEC Visualizers](https://github.com/john-friedman/SEC-Visualizers)

### Quickstart
Load package
```
from sec_parsers import Filing
```

Downloading html file (new)
```
from sec_downloaders import SEC_Downloader

downloader = SEC_Downloader()
downloader.set_headers("John Doe", "johndoe@example.com")
download = downloader.download(url)
filing = Filing(download)
```

Downloading html file (old)
```
from sec_parsers download_sec_filing
html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1318605/000162828024002390/tsla-20231231.htm')
filing = Filing(html)
```

Parsing
```
filing.parse() # parses filing
filing.visualize() # opens filing in webbrowser with highlighted section headers
filing.find_sections_from_title(title) # finds section by title, e.g. 'item 1a'
filing.find_sections_from_text(text) # finds sections which contains your text
filing.get_tree(node) # if no argument specified returns xml tree, if node specified, returns that nodes tree
filing.get_title_tree() # returns xml tree using titles instead of tags. More descriptive than get_tree.
filing.get_subsections_from_section() # get children of a section
filing.get_nested_subsections_from_section() # get descendants of a section
filing.set_filing_type(type) # e.g. 'S-1'. Use when automatic detection fails
filing.save_xml(file_name,encoding='utf-8')
filing.save_csv(file_name,encoding='ascii')
```
### Additional Resources:
* [quickstart](Examples/quickstart.ipynb)
* [How to write a Custom Parser in 5 minutes](https://medium.com/@jgfriedman99/how-to-write-a-custom-sec-parser-in-5-minutes-5c7a8d5d81b0)
* [Archive of Parsed XMLs / CSVs](https://www.dropbox.com/scl/fo/np1lpow7r3bissz80ze3o/AKGM8skBrUfEGlSweofAUDU?rlkey=cz1r78jofntjeq4ax2vb2yd0u&e=1&st=mdcwgfcm&dl=0) - Last updated 7/24/24.
* [example parsed filing](Examples/tesla_10k.xml)
* [example parsed filing exported to csv](Examples/tesla_10k.csv).

### Features:
* lots of filing types
* export to xml, csv, with option to convert to ASCII
* visualization

### Feature Requests:
[Request a Feature](contributors.md)
* company metadata (sharif) - will add to downloader
* filing metadata (sharif) - waiting for SEC Downloaders first release
* Export to dta (Denis)
* DEF 14A, DEFM14A (Denis)
* Export to markdown (Astarag)
* Better parsing_string handling. Opened an issue. (sharif)


### Other packages useful for SEC filings
* https://github.com/dgunning/edgartools

### Updates
#### Towards Version 1:
Note: next major update will happen in august. It will improve quality of parsing, and dramatically increase speed.
Changes: streaming, combined detectors (e.g. all caps / emphasis cap with handling for unique cases), one use detectors, adding parse_id, merging clean parse,
xml tree construct into one function.

* Most/All SEC textual filings supported

Might be done along the way:
* Faster parsing, probably using streaming approach, and combining modules together.
* Introduction section parsing
* Signatures section parsing
* Better visualization interface (e.g. like pdfviewer for sections)

#### Beyond Version 1:
To improve the package beyond V1 it looks like I need compute and storage. Not sure how to get that. Working on it.

Metadata
* Clustering similar section titles using ML (e.g. seasonality headers)
* Adding tags to individual sections using small LLMs (e.g. tag for mentions supply chains, energy, etc)

Other
* Table parsing
* Image OCR
* Parsing non-html filings

### Current Priority list:
* look at code duplication w.r.t to style detectors, e.g. all caps and emphasis. may want to combine into one detector
- yep this is a priority. have to handle e.g. Introduction and Segment Overview as same rule. Bit difficult. Will think over.
* better function names - need to decide terminology soon.
* consider adding table of contents, forward looking information, etc
- forward looking information, DOCUMENTS INCORPORATED BY REFERENCE, TABLE OF CONTENTS - go with a bunch, 
* fix layering issue - e.g. top div hides sections
* make trees nicer
* add more filing types
* fix all caps and emphasis issue
* clean text
* Better historical conversion: handle if PART I appears multiple times as header, e.g. logic here item 1 continued.


