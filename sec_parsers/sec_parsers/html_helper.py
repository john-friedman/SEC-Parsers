import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag
import random
import pandas as pd

    
# Parsing #
def get_elements_between_two_elements(elem1, elem2):
    """Get all elements between two beautiful soup tags. if elem2 is None, get all elements after elem1."""
    end_bool = False
    elements = []

    item = elem1.next
    while not end_bool:
        if elem2 is None:
            if item is None:
                end_bool = True
            else:
                if isinstance(item, Tag):
                    elements.append(item)
                # go to next item
                item = item.next
        else:
            if item == elem2:
                end_bool = True
            else:
                if isinstance(item, Tag):
                    elements.append(item)
            # go to next item
            item = item.next
    return elements

# tested
# add cleaning later
def get_text_between_two_elements(elem1, elem2):
    """Get the text between two beautiful soup tags. If elem2 is None, get all text after elem1."""
    end_bool = False
    text = ''

    item = elem1.next
    while not end_bool:
        if elem2 is None:
            if item is None:
                end_bool = True
            else:
                if isinstance(item, NavigableString):
                    # apply cleaning
                    text += item
                # go to next item
                item = item.next
        else:
            if item == elem2:
                end_bool = True
            else:
                if isinstance(item, NavigableString):
                        # apply cleaning
                        text += item
                # go to next item
                item = item.next
    return text

# works for now, but should do robustness checks - easy to catch
def detect_table_of_contents(element):
    """Detects if a table is likely to be a table of contents."""
    # get number of links
    links = element.find_all('a')
    if len(links) > 5:
        return True

# will need a bunch of work. This is our workhorse.
def handle_table_of_contents(soup):
    """Handles the table of contents in a sec 10k, returns a dictionary."""
    tables = soup.findAll('table')
    table_of_contents_detected = False
    for table in tables:
        if detect_table_of_contents(table):
            table_of_contents_detected = True
            break

    if not table_of_contents_detected:
        raise ValueError('Table of contents not detected')
    
    rows = table.find_all('tr')
    # preprocessing - remove all empty rows
    rows = [row for row in rows if row.text.strip() != '']
    table_of_contents_dict = {'parts': []}
    # iterate through rows
    part = ''
    for row in rows:
        if 'part' in row.text.lower():
            # clean part name
            part_name = re.sub('\s+','',row.text.lower().strip())

            part = {'name': part_name, 'href': row.find('a')['href'], 'items': []}
            table_of_contents_dict['parts'].append(part)
        
        elif 'item' in row.text.lower():
            item_text = row.text.lower().strip()
            item_name = re.search('Item[\s+][0-9]{1,}[A-Z]{0,}(?=[\.|\s+|$])', item_text, re.IGNORECASE).group(0)
            # clean item name
            item_name = re.sub('\s+','',item_name)
            # remove item name from item text
            item_text = item_text.replace(item_name, '')
            # cleanup by removing leading and trailing whitespace, periods
            item_text = item_text.strip().strip('.')

            item_desc = re.search('^.*?(?=\d+$)', item_text, re.IGNORECASE).group(0)
            item = {'name': item_name, 'desc': item_desc, 'href': row.find('a')['href']}
            part['items'].append(item)

    
    return table_of_contents_dict
    
def detect_subheadings(elements):
    subheadings_element_list = []
    return subheadings_element_list


# Visualizations # 
def open_soup(soup):
    """Opens a beautiful soup object in a web browser."""
    html = str(soup)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8-sig") as f:
        url = 'file://' + f.name
        f.write(html)
    webbrowser.open(url)

def generate_pastel_colors(n):
  """Generates a list of n pleasant pastel background colors.

  Args:
      n: The number of colors to generate.

  Returns:
      A list of n hexadecimal color strings representing pastel colors.
  """
  pastel_range = (210, 255)  # Range for pastel color lightness
  pastel_saturation = (0.3, 0.8)  # Range for pastel color saturation
  colors = []
  for _ in range(n):
    red = random.randint(*pastel_range)
    green = random.randint(*pastel_range)
    blue = random.randint(*pastel_range)
    saturation = random.uniform(*pastel_saturation)
    # Convert to hexadecimal string with "#" prefix
    color = f"#{red:02x}{green:02x}{blue:02x}"
    colors.append(color)
  return colors

def add_style(element, css_style,replace = False):
    """adds a css style to a beautiful soup element."""
    if replace:
        element['style'] = css_style
    else:
        if element.get('style') is None:
            element['style'] = css_style
        else:
            element['style'] += ';' + css_style





