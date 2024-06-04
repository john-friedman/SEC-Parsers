![Screenshot 1](Screenshots/1.png)

Project to learn how to use Python's Beautiful Soup Library, as well as to understand how unstructured text can be stored in html documents.

This project was difficult due to the extreme lack of standardization, followed by complications such as one element of a word being unbolded
and the rest being bolded. I suspect the complications are a deliberate attempt by companies / the filing contractors to make it harder
to machine read the filings.

The project has mixed success. Most SEC 10-k filings can be parsed well, with minor issues such as missing some text here or there.

I'll attempt to parse SEC 10-Ks again in the future.



![Screenshot 1](Screenshots/header.png)
![Screenshot 1](Screenshots/2.png)
![Screenshot 1](Screenshots/3.png)


Notes on BeautifulSoup:
* duplication of functions. Looking up resources online to mixed results, better to just read original code.
```
    findNextSiblings = find_next_siblings   # BS3
    fetchNextSiblings = find_next_siblings  # BS2
```