## SEC Parsers
![PyPI - Downloads](https://img.shields.io/pypi/dm/sec-parsers)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fhttps%2F%2Fgithub.com%2Fjohn-friedman%2FSEC-Parsers&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![GitHub](https://img.shields.io/github/stars/john-friedman/sec-parsers)

Parses non-standardized SEC filings into structured xml. Use cases include LLMs, NLP, and textual analysis. Average parse-time for a 100 page document is 0.4 seconds. Package is a WIP.

Supported filing types are 10-K, 10-Q, 8-K, S-1, 20-F. More will be added soon, or you can write your own! [How to write a Custom Parser in 5 minutes](https://medium.com/@jgfriedman99/how-to-write-a-custom-sec-parser-in-5-minutes-5c7a8d5d81b0)

Note: syntax change for find_nodes_by_title, to find_all_sections_by_title and associated functions.

<em>URGENT</em>: Advice on how to name functions used by users is urgently needed. SEC Parsers has started to get users, and I don't want to deprecate function names in the future. [Link](contributors.md)

<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_visualizationv3.png">
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_tree_v4.png" width="500">
</div>

Installation
```
pip install sec-parsers
```

Quickstart
```
from sec_parsers import Filing, download_sec_filing

html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1318605/000162828024002390/tsla-20231231.htm')
filing = Filing(html)
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
* \[In Progress\] Article explaining how to write custom filing parsers.
* [Archive of Parsed XMLs / CSVs](https://www.dropbox.com/scl/fo/np1lpow7r3bissz80ze3o/AKGM8skBrUfEGlSweofAUDU?rlkey=cz1r78jofntjeq4ax2vb2yd0u&e=1&st=mdcwgfcm&dl=0) - Last updated 7/24/24.
* [example parsed filing](Examples/tesla_10k.xml)
* [example parsed filing exported to csv](Examples/tesla_10k.csv).

### Features:
* lots of filing types
* export to xml, csv, with option to convert to ASCII
* visualization

### Feature Requests:
[Request a Feature](contributors.md)
* Export to dta (Denis)
* DEF 14A, DEFM14A (Denis)
* Export to markdown (Astarag)
* Better parsing_string handling. Opened an issue. (sharif)

### Statistics
* Speed: On average, 10-K filings parse in 0.25 seconds. There were 7,118 10-K annual reports filed in 2023, so to parse all 10-Ks from 2023 should take about half an hour.

### Updates
#### Towards Version 1:
* Most/All SEC text filings supported
* Few errors
* xml 

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
* Fix xml tree issue with parsing type
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


