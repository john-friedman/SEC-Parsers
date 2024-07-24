# SEC Parsers
Parses non-standardized SEC filings into structured xml. Use cases include LLMs, NLP, and textual analysis. Package is a WIP.

Supported filing types are 10-K, 10-Q, 8-K. More will be added soon.

<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_visualizationv3.png">
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_tree_v3.png" width="500">
</div>

### Statistics
* Speed: On average, 10-K filings parse in 0.25 seconds. There were 7,118 10-K annual reports filed in 2023, so to parse all 10-Ks from 2023 should take about half an hour.

# Patch notes:
* added warnings for set headers, and for automatic filing type detection
* Parse speed increased more than 10X

## Resources
quickstart link
jupyter notebook link
dropbox link
medium article for defining custom parsers

## Add table of contents
* add contributions?

## Shortterm TODO:
* Add S-1 filings, and others
* fix all caps emphasis issue

## Midterm TODO:
* More detailed XML tree
* Faster XML conversion
* Better historical conversion: handle if PART I appears multiple times as header, e.g. logic here item 1 continued.

## Future speed:
* switching from memory to streaming / common sense fixes. don't need now as its fast enough

## Roadmap:
v1 - parses most/all sec text filings well into detailed xml trees.

## Future updates:  
* Better filing element handling: e.g. table handling, OCR on images stored on static site
* Analysis: sections clustering (e.g. Seasonality, Seasonal Variance)
* Better metadata: I'm considering running a small LLM to tag section titles, and sections text. e.g. Section title 'Marketing and Sales' might often contain supply chain details. Or for example, specific section in Tesla 10k is 2000chars that say text found elsewhere.
* Backwards compatability for non-html files.

Some of these updates require significant compute resources / file hosting, which I currently lack.

## Feature Request:
To request features or suggest a way to improve the package please use the form below.
[Google Form](https://forms.gle/cCh7VT93v4tV4ekp8)
* Extract title of section along with its text (sharif)
* Extract subsections from section (sharif)
* Export to dta (Denis)
* option to remove special chars from document in export (bill mcdonald)

## Updated Quickstart
link to jupyter notebook, links to dropbox for parsed xml sample

## Problem
SEC filings are complex and mostly non-standardized...

## How SEC Parsers works


## Alternatives fill out
* Bill mcdonald 10k regex
* sec-api regex
* unstructured.io - I don't know how this works yet
* noteblocks (or is it textblocks)
* cybersyn



// Vanity
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fhttps%2F%2Fgithub.com%2Fjohn-friedman%2FSEC-Parsers&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)