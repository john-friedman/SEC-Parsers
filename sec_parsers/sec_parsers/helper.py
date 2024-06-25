import re
import tempfile
import webbrowser
from bs4 import BeautifulSoup, NavigableString, Tag
import random
import pandas as pd


# File to store helper functions for parsing SEC files


    
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