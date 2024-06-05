![Screenshot 1](Screenshots/1.png)

Project to learn how to use Python's Beautiful Soup Library, as well as to understand how unstructured text can be stored in html documents.

This project was difficult due to the extreme lack of standardization, followed by complications such as one element of a word being unbolded and the rest being bolded. I suspect that some of the complications are a deliberate attempt by companies / the filing contractors to make it harder to machine read the filings.

Currently the project has multiple iterations of parsers
1. parsers based on text only, with a tool to help check if parsing is mostly correct
2. parsers based on elements using decompose
3. parsers based on element implementing highlighting
4. parsers based on iterating through the tree recursively, and simplifying the html [current]

Each iteration of the parsers reflects my better understanding of how to use beautiful soup.

![Screenshot 1](Screenshots/header.png)
![Screenshot 1](Screenshots/2.png)
![Screenshot 1](Screenshots/3.png)


Notes on BeautifulSoup:
* duplication of functions. Looking up resources online to mixed results, better to just read original code.
```
    findNextSiblings = find_next_siblings   # BS3
    fetchNextSiblings = find_next_siblings  # BS2
```