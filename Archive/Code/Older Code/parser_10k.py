from bs4 import BeautifulSoup, NavigableString, Tag
import re

from helper import open_soup, detect_unique_text, add_style, add_class, check_if_ancestor_has_class, is_paragraph



def parse_10k(path, open_cleaned=False):
    with open(path) as f:
        html = f.read()

    # apply some preprocessing to clean up non standard characters
    html = re.sub(r'([\s+]|(\&nbsp;*)){1,}', ' ', html)

    soup = BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    # remove existing background colors from all elements
    for element in body.find_all():
        if element.has_attr("style"):
            element['style'] = re.sub(r'background-color:[^;]{1,}','',element['style'])

    # remove hidden elements
    # may need to tweak
    for element in body.select('[style*="display: none"]'):
        element.decompose()

    # remove all classes from all elements
    for element in body.find_all():
        if element.has_attr("class"):
            del element['class']        

    # Mark all <hr> tags
    for tag in body.find_all("hr"):
        add_class(tag, "hr")
    
    # Mark all table of content links
    for tag in body.find_all('a', string= re.compile(r'Table of Contents', re.IGNORECASE)):
        add_class(tag, "toc")

    # Mark all tables 
    for tag in body.find_all("table"):
        if not '\xa0' in tag.text:
            # check if fake table, e.g. header
            if detect_unique_text(tag):
                add_class(tag, "section_title")
            else:
                add_class(tag, "table")
        else:
            # check if real table
            add_class(tag, "table")

    # Mark all elements relating to tables " table "
    for tag in body.find_all(string= re.compile(r' table ', re.IGNORECASE)):
        add_class(tag.parent, "table")

    # Mark all elements with no text
    for element in body.find_all():
        text = element.text.strip()
        if ((text == "") | (text =="&nbsp;")):
            add_class(element, "empty")

    # check if is paragraph
    for element in body.find_all(recursive=True):
        if is_paragraph(element):
            #if not check_if_ancestor_has_class(element):
            add_class(element, "section_text")

    # Mark all headers
    for element in body.find_all(recursive=True):
        if detect_unique_text(element):
            # important to check for tables
            if not check_if_ancestor_has_class(element):
                add_class(element, "section_title")

    

    # Color classes
    color_list = ['Cornsilk','BlanchedAlmond','Bisque','NavajoWhite','Wheat','BurlyWood','Tan','RosyBrown','SandyBrown','Goldenrod','DarkGoldenrod','Peru','Chocolate','SaddleBrown','Sienna','Brown','Maroon']
    color_dict = {'section_title':'LightPink','section_text':'LightSkyBlue','preamble':'MistyRose'}
    for element in body.find_all(attrs={'class': True}):
        element_class = element['class']
        if element_class in color_dict.keys():
            add_style(element, f"background-color:{color_dict[element_class]};")
        else:
            color = color_list.pop(0)
            color_dict[element_class] = color
            add_style(element, f"background-color:{color};")
        



    if open_cleaned:
        open_soup(soup)

    return soup
    

