# SEC Parsers
Parses non-standardized SEC 10-K filings into well structured detailed xml. This is a WIP. Not every file will parse correctly.

![](https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_visualization.png)
![](https://raw.githubusercontent.com/john-friedman/SEC-Parsers/main/Assets/tesla_tree_v2.png)

### Installation
```pip install sec-parsers```

### Quickstart
```
from sec_parsers import *

html = download_sec_filing('https://www.sec.gov/Archives/edgar/data/1318605/000162828024002390/tsla-20231231.htm')
parsed_html = parse_10k(html)
xml = construct_xml_tree(parsed_html)
```

For more information look at the [quickstart](Examples/quickstart.ipynb), or view a parsed Tesla 10-K [here](Examples/tesla.xml).

### Links:
* [GitHub](https://github.com/john-friedman/SEC-Parsers/)
* [Archive of Parsed XMLs](https://www.dropbox.com/scl/fo/np1lpow7r3bissz80ze3o/AKGM8skBrUfEGlSweofAUDU?rlkey=cz1r78jofntjeq4ax2vb2yd0u&e=1&st=mdcwgfcm&dl=0) - Note: This is often out of date, as package is being updated frequently.

### Problem:
When you look at an SEC 10-K you can easily see the structure of the file, and what headers follow each other. Under the hood, these filings are non-standardized making it hard to convert into a well structured format suitable for NLP/RAG.

### How SEC Parsers works:
1. Detects headers in filings using:
* element tags, e.g. `<b>Item 1</b>`
* element css, e.g. `<p style="font-weight: bold;">Item 1.</p>`
* text style, e.g. emphasis style "Purchase of Significant Equipment"
* relative location of above elements to each other
2. Calculates hierarchy of headers, and converts to a tree structure

### Priority TODO
2. Get Input on design, etc
1. fix title / rearrange classes, etc
3. organize and clean code
4. csv export option

### Roadmap:
1. Detailed parser with better than 99% success rate (currently hovering around 90).
2. Clustering on cleaned xml files (e.g. many companies have a seasonality heading but its named differently), add an attribute to help sort by this

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

### Statistics
Not implemented yet.

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
* Computer Vision using OpenCV
* LLMs (I believe unstructured.io does something like this)
* Transformers 
