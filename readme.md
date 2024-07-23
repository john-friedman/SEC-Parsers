# SEC Parsers
Parses non-standardized SEC 10-K filings into well structured detailed xml. Use cases include LLMs, NLP, and textual analysis. 

# Patch notes:
* added warnings for set headers, and for automatic filing type detection
* Parse speed increased. e.g. 183 page filing that took 7s to parse now takes .26s.

## Statistics
* How long it takes to parse x file, 
* What percentage of 10ks parse

## Updated Visuals

## Resources
quickstart link
jupyter notebook link
dropbox link
medium article for defining custom parsers

## Add table of contents
* add contributions?

## Shortterm TODO:
* Add S-1 filings, and others

## Midterm TODO:
* More detailed XML tree
* Faster XML conversion
* Better historical conversion: handle if PART I appears multiple times as header, e.g. logic here item 1 continued.

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
![Google Form](https://forms.gle/cCh7VT93v4tV4ekp8)
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