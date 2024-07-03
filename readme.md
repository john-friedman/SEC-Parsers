# SEC Parsers
Parses non-standardized SEC 10-K filings into well structured xml. This is a WIP. Not every file will parse correctly.


### Quickstart (add images/output)
```
download
parse
visualize
convert to xml
print structure by title, by desc (attributes)
get text by node (this includes desc)
save to xml
```

### Link to storage with sample parsed xmls 


### Problem:
When you look at an SEC 10-K you can easily see the structure of the file, and what headers follow each other. Under the hood, these filings are non-standardized making it hard to convert into a well structured format suitable for NLP/RAG.

### How SEC Parsers works:
1. Detects headers in filings using:
* element tags, e.g. <b>Item 1</b>
* element css, e.g. <p style="font-weight: bold;">Item 1.</p>
* text style, e.g. emphasis style "Purchase of Significant Equipment"
* relative location of above elements to each other
2. Calculates hierarchy of headers, and converts to a tree structure


### Future
* fix titles for xml (e.g. item 1 instead of item 1. business)
* better hierarchy calculation
* more supported filings: 10-Q, 8-K, etc
* better rag integration
* converting html tables to nice xml tables
* metadata, e.g. cik / data from xbrl in html
* hosting cleaned xml files online
* better attributes (names / format)
* better color scheme (color scheme for headers, ignored_elements - e.g. page numbers, text)
* better function naming
* better modules naming
* better parent handling
* better descriptions of functions
* better github and pypi pages

### TODO
* finish useful functions code
* test on sample data
* push to pip and github
* check dependencies are fine and download works on other machines
* update jupyter notebooks
* update old stackoverflow answers
* check user needs

### Statistics

### Some Other Packages that might be useful:
* [edgartools](https://github.com/dgunning/edgartools) - good interface for interacting with SEC's EDGAR system

### Alternative Approaches to Parsing SEC Filings
* [sec-parser](https://github.com/alphanome-ai/sec-parser) - oops, we have similar names. They were first, my bad. They parse 10-Qs well.
* [sec-api](https://sec-api.io/). Paid API to search / download SEC filings. Basically, SEC's EDGAR but setup in a much nicer format. I haven't used it since it costs money.
* [Bill McDonald's 10-X Archive](https://sraf.nd.edu/data/stage-one-10-x-parse-data/)
* OpenCV
* LLMs (I believe unstructured.io does something like this)
* Transformers 