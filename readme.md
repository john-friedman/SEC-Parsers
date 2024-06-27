# Experimental Branch

## TODO:
1. ~~test new approach to parsing on something handles tables is good at. get parser working~~
2. Improve toc handling - using tests
3. better names - maybe look up another package for inspiration? e.g. 
4. utils? / _ in front of helper names
5. misc QOL features
6. visualization
7. better github structure 
8. upload to test pypi and update main branch with notice of experimental branch
9. TESTS. I have 1k 10k sec filings from last 90 days on my computer. see how many parse, then dig in to see how well.
10. benchmarks (mostly how many 10k parsed etc), but some for time taken
* better visualization will do wonders here - maybe make pyqt gui to compare side by side?

Before pushing experimental to main, remember to update jupyter notebooks / stackoverflow answers.

Everything is WIP rn, so structure is fluid. Figure out good naming conventions and how to hide / show functions in packages.

TODO:
consider using lxml html parser - it takes ~2-4 seconds to parse a file into xml. 
could be because i'm doing something dumb, but I think a decent amount of overhead is from beautiful soup. 