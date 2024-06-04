import re
from bs4 import BeautifulSoup as Soup

html = '''
<html><body><p>This is a paragraph</p></body></html>
'''

soup = Soup(html)
text = soup.p.string
soup.p.clear()
print(soup)

match = re.search(r'\ba\b', text)
start, end = match.start(), match.end()


b = soup.new_tag('b')
b['style'] ="background-color:powderblue;"
b.append(text[start:end])
soup.p.append(b)

# add last part
soup.p.append(text[end:])

print(soup)

import tempfile
import webbrowser
html = str(soup)
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    url = 'file://' + f.name
    f.write(html)
webbrowser.open(url)