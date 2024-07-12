# SEC Parsers
Parses non-standardized SEC 10-K filings into well structured detailed xml. Use cases include LLMs, NLP, and textual analysis. This is a WIP. Not every file will parse correctly. Support for 10Q filings temporarily removed.

<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_visualization.png">
</div>
<div align="center">
  <img src="https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_tree_v2.png" width="500">
</div>


### Installation
```pip install sec-parsers```

### Quickstart
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

For more information look at the [quickstart](Examples/quickstart.ipynb), or view a parsed Tesla 10-K [here](Examples/tesla_10k.xml). SEC Parsers also supports exporting to csv, see [here](Examples/tesla_10k.csv).

### Links: 
* [GitHub](https://github.com/john-friedman/SEC-Parsers/)
* [Archive of Parsed XMLs / CSVs](https://www.dropbox.com/scl/fo/np1lpow7r3bissz80ze3o/AKGM8skBrUfEGlSweofAUDU?rlkey=cz1r78jofntjeq4ax2vb2yd0u&e=1&st=mdcwgfcm&dl=0) - Last updated 7/10/24.

### Problem:
SEC filings are human readable, but messy html makes it hard for machines to detect and read information by section. This is especially important for NLP / RAG using LLMs.

### How SEC Parsers works:
1. Detects headers in filings using:
* element tags, e.g. `<b>Item 1</b>`
* element css, e.g. `<p style="font-weight: bold;">Item 1.</p>`
* text style, e.g. emphasis style "Purchase of Significant Equipment"
* relative location of above elements to each other
2. Calculates hierarchy of headers, and converts to a tree structure

### Roadmap:
1. Parser that converts >95% of filings into nicely formatted xml trees. Currently at 90%.
2. Apply data science on xml to cluster headers, e.g. seasonality, seasonal variation etc, to make xml easier to work with.

### Possible future features
* better hierarchy calculation
* more filings supported
* better rag integration
* converting html tables to nice xml tables
* hosting cleaned xml files online
* better color scheme (color scheme for headers, ignored_elements - e.g. page numbers, text)
* better descriptions of functions

### Features
* Parse 10K
* Export to XML, CSV
* XBRL metadata

### Feature request:
* save_dta - save xml to dta. similar to csv function
* better selection by titles. e.g. selecting by item1, will also return item 1a,... not sure how to set this up in a nice way
* More XBRL stuff

### Statistics
* 100% parsed html rate
* 90% conversion to xml rate. This is better than it seems as there are a few companies like Honda owner trust which do not parse but have ~10 10ks per year. (e.g. trust 1, 2,...,)
* On average ~1s to parse file (range .1s-3s)

### Issues
1. handle if PART I appears multiple times as header, e.g. logic here item 1 continued. Develop logic to handle this. Probably in cleanup?

### TODO
1. improve construct xml tree. add signatures, and intro (better name needed) sections
2. metadata parsing
0. we fixed one table issue, now need to account for too much tables https://www.sec.gov/Archives/edgar/data/18255/000001825518000024/cato10k2017-jrs.htm
2. Code cleanup. Right now I'm tweaking code to increase parse rate, eventually need to incorporate lessons learned, and rewrite.

### Other people's SEC stuff
* [edgartools](https://github.com/dgunning/edgartools) - good interface for interacting with SEC's EDGAR system
* [sec-parser](https://github.com/alphanome-ai/sec-parser) - oops, we have similar names. They were first, my bad. They parse 10-Qs well.
* [sec-api](https://sec-api.io/). Paid API to search / download SEC filings. Basically, SEC's EDGAR but setup in a much nicer format. I haven't used it since it costs money.
* [Bill McDonald's 10-X Archive](https://sraf.nd.edu/data/stage-one-10-x-parse-data/)
* [Eclect](https://eclect.us/) - "Save time reading SEC filings with the help of machine learning.". Paid.
* [Textblocks.app](https://www.textblocks.app/) - Paid API to extract and analyze structured data from SEC filings. The approach seems to be similar to mine.
* [Yu Zhu](https://yuzhu.run/how-to-parse-10x/) - article with an approach to parse 10K filings using regex
* [Wharton Research Data Services](https://wrds-www.wharton.upenn.edu/pages/grid-items/sec-analytics-suite/) - heard they have SEC stuff, looking into it
* [Gist](https://gist.github.com/anshoomehra/ead8925ea291e233a5aa2dcaa2dc61b2) - using regex and beautifulsoup to parse 10Ks
* [Victor Dahan](https://opencodecom.net/post/2021-08-18-sentiment-analysis-of-10-k-files/) - Sentiment Analysis of 10-K Files
* [edgarWebR](https://mwaldstein.github.io/edgarWebR/) - edgarWebR provides an interface to access the SEC’s EDGAR system for company financial filings.
* [NLP in the stock market](https://towardsdatascience.com/nlp-in-the-stock-market-8760d062eb92) - Leveraging sentiment analysis on 10-k fillings as an edge
* Computer Vision using OpenCV
* LLMs (I believe unstructured.io does something like this)
* Transformers 
