import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag
import random
import pandas as pd


# File to store helper functions for parsing SEC files

def detect_table_of_contents(element):
    """Detects if a table is likely to be a table of contents."""
    # get number of links
    links = element.find_all('a')
    if len(links) > 5:
        return True
    
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

def get_text_between_Tags(elem1, elem2,background_color = True, clean=True):
    """Get the text between two beautiful soup tags. """
    end_bool = False
    text = ''

    if background_color:
        pass
        #add_style(elem1.parent, f"background-color:Olive;")

    item = elem1.next
    while not end_bool:
        if item == elem2:
            if background_color:
                pass
                #add_style(elem2.parent, f"background-color:Olive;")
            end_bool = True
        else:
            if isinstance(item, NavigableString):
                if clean == True:
                    cleaned_item_text = item.text.strip()
                    if cleaned_item_text != '':
                        text += cleaned_item_text + '\n'
                else:
                    text += item
            else:
                if background_color:
                    add_style(item, f"background-color:{background_color};")
        # go to next item
        item = item.next
    return text

def handle_table_of_contents(soup):
    """Handles the table of contents in a sec 10k"""
    tables = soup.findAll('table')
    table_of_contents_detected = False
    for table in tables:
        if detect_table_of_contents(table):
            table_of_contents_detected = True
            break

    if not table_of_contents_detected:
        raise ValueError('Table of contents not detected')
    
    # parse table of contents
    # if top item has no page number is probably part
    # item rows have item (SEC), item title and link (exact name changes), and page number

    # get all rows
    tables_rows = table.find_all('tr')
    # select rows which have text
    table_rows = [row for row in tables_rows if row.text.strip() != '']

    row_dict_list =[]
    part = ''
    for table_row in table_rows:
        # first check if element is table of contents link
        if 'table of contents' in table_row.text.strip().lower():
            continue

        # handle parts
        if re.search(r'^part', table_row.text.strip(), re.IGNORECASE) is not None:
            part = re.sub('\s+',' ',table_row.text.strip())

            part = re.search(r'^part\s+(i(\s+|$|\.)|ii(\s+|$|\.)|iii(\s+|$|\.)|iv(\s+|$|\.))', part, re.IGNORECASE).group(0).strip()
            part = re.sub(r'\.$','',part)

        # handle items
        row = {}
        row['part'] = part
        # Parse as item
        for cell in table_row.find_all('td'):
            # item
            if re.search(r'^(item|signatures)', cell.text.strip(), re.IGNORECASE) is not None:
                row['item'] = re.search("^[^.]+",re.sub('\s+',' ', cell.text.strip())).group(0)

            # link
            if cell.find('a') is not None:
                row['link_text'] = cell.find('a').text
                row['href'] = cell.find('a')['href']

        if len(row) > 1:
            row_dict_list.append(row)

    # convert to dataframe
    df = pd.DataFrame(row_dict_list)

    # drop nan
    # note: in the future, we may want to handle this more gracefully
    df = df.dropna()
    # reset index
    df = df.reset_index(drop=True)
    
    # clean names
    df['item'] = df['item'].apply(lambda x: re.sub('[^a-zA-Z0-9\n\.]', '', x)).str.replace('.','').str.lower()
    df['part'] = df['part'].apply(lambda x: re.sub('[^a-zA-Z0-9\n\.]', '', x)).str.replace('.','').str.lower()
    return df


# visualization
def print_xml_structure(tree):
    root = tree.getroot()

    def indent(level):
      return "  " * level

    def print_element(element, level):
      print(indent(level) + element.tag)
      for child in element:
        print_element(child, level + 1)

    print_element(root, 0)

def extract_text(element):
    text = ''
    if element.text is not None:
        text = element.text.strip()
    for child in element:
        text += extract_text(child)
    
    return text