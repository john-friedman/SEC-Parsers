# SEC Parsers
Parses non-standardized SEC 10-K filings into well structured detailed xml. Use cases include LLMs, NLP, and textual analysis. 

TODO:
* reduce number of variables and rename for detectors
* add dynamic handling of xml construction based on object
* reduce error rate back to normal levels (less than 1 pct)
* Add more supported filings: S1 first
* add warnings for set headers and automatic type detection

GitHub TODO
* Readme readability revamp
* file supported
* speed - less than a second avg, code not optimized, will be reduced
* how to install
* quickstart
* export to csv, xml etc
* how to define custom parsers
* Links github dropbox
* Problem clearly stated
* How SEC Parsers works
* Roadmap
* statistics

Future:
* image OCR / hosting (FAR)
* visualizer rewrite - e.g. pdf viewer but for headers
* table handling (I think can probably get to 95% table handling relatively easily)

Package Roadmap
* Stage 1: Support a lot of filing types with >99% parse rate, and very detailed trees without errors
* Stage 2: cluster headers e.g. season seasonal variation
* Stage 3: LLMS + OCR on filings, e.g. to see if section just says nothing here, or e.g. to describe image
* Stage 4: backwards compatability for text files

How people can help:
* Better color scheme suggestion for visualizer
* Hosting for parsed files (future)
* suggestions for better RAG for LLMS
* suggestions for other metadata
* qol improvements, e.g. for finding titles etc within parsed xml


Feature request:
* save_dta - save xml to dta. similar to csv function

Issues
1. handle if PART I appears multiple times as header, e.g. logic here item 1 continued.

Better format below, and add more:
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

### Other people's papers related to SEC stuff
* [Sentiment Analysis on 10-K Financial Reports using Machine Learning Approaches](https://ieeexplore.ieee.org/document/9612552)

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fhttps%2F%2Fgithub.com%2Fjohn-friedman%2FSEC-Parsers&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)