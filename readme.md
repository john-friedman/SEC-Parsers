## SEC Parsers
Parses non-standardized SEC filings into structured xml. Use cases include LLMs, NLP, and textual analysis. Package is a WIP.

Supported filing types are 10-K, 10-Q, 8-K. More will be added soon.

// Vanity
![PyPI - Downloads](https://img.shields.io/pypi/dm/sec-parsers)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fhttps%2F%2Fgithub.com%2Fjohn-friedman%2FSEC-Parsers&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_visualizationv3.png">
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_tree_v3.png" width="500">
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
filing.find_nodes_by_title(title) # finds node by title, e.g. 'item 1a'
filing.find_nodes_by_text(text) # finds nodes which contains your text
filing.get_tree(node) # if no argument specified returns xml tree, if node specified, returns that nodes tree
filing.get_title_tree() # returns xml tree using titles instead of tags. More descriptive than get_tree.
filing.save_xml(file_name)
filing.save_csv(file_name)
```
Additional Resources:
* [quickstart](Examples/quickstart.ipynb)
* medium article to define custom parsers
* [Archive of Parsed XMLs / CSVs](https://www.dropbox.com/scl/fo/np1lpow7r3bissz80ze3o/AKGM8skBrUfEGlSweofAUDU?rlkey=cz1r78jofntjeq4ax2vb2yd0u&e=1&st=mdcwgfcm&dl=0) - Last updated 7/10/24.
* [example parsed filing](Examples/tesla_10k.xml)
* [example parsed filing exported to csv](Examples/tesla_10k.csv).

Links
* [GitHub](https://github.com/john-friedman/SEC-Parsers/)

Statistics
* Speed: On average, 10-K filings parse in 0.25 seconds. There were 7,118 10-K annual reports filed in 2023, so to parse all 10-Ks from 2023 should take about half an hour.


### Updates
Patch notes:
* added warnings for set headers, and for automatic filing type detection
* Parse speed increased more than 10X

Shortterm TODO:
* Add S-1 filings, and others
* fix all caps emphasis issue

Midterm TODO:
* More detailed XML tree
* Faster XML conversion
* Better historical conversion: handle if PART I appears multiple times as header, e.g. logic here item 1 continued.

Future performance:
* switching from memory to streaming / common sense fixes. don't need now as its fast enough

#### Roadmap:
v1 - parses most/all sec text filings well into detailed xml trees.

Future updates:  
* Better filing element handling: e.g. table handling, OCR on images stored on static site
* Analysis: sections clustering (e.g. Seasonality, Seasonal Variance)
* Better metadata: I'm considering running a small LLM to tag section titles, and sections text. e.g. Section title 'Marketing and Sales' might often contain supply chain details. Or for example, specific section in Tesla 10k is 2000chars that say text found elsewhere.
* Backwards compatability for non-html files.

Some of these updates require significant compute resources / file hosting, which I currently lack.

Feature Request:
To request features or suggest a way to improve the package please use the form below.
[Google Form](https://forms.gle/cCh7VT93v4tV4ekp8)
* Extract title of section along with its text (sharif)
* Extract subsections from section (sharif)
* Export to dta (Denis)
* option to remove special chars from document in export (bill mcdonald)


## Problem
SEC filings are complex and mostly non-standardized...

## How SEC Parsers works

## Alternatives fill out
* Bill mcdonald 10k regex
* sec-api regex
* unstructured.io - I don't know how this works yet
* noteblocks (or is it textblocks)
* cybersyn



