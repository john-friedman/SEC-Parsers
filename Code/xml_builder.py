from helper import add_style


def xml_builder(soup,visualize=False):
    """Visualize opens chrome tab with the colored soup object"""
    pass

def color_parsing(soup):
    # https://www.htmlcodes.ws/color/html-color-code-generator.cfm?colorName=PowderBlue


    # we'll add gradient colors later in the distinguishing headers update
    color_dict = {'header':'BurlyWood','section_text':'Wheat','empty':'LightYellow','skipping':'Pink'}

    for element in soup.find_all(attrs={'class': True}):
        element_class = element['class']

        # there will be weird visualization errors here. This is sloppy
        if element_class == 'empty':
            add_style(element, f"background-color:{color_dict['empty']};")
        elif element_class == 'header':
            add_style(element, f"background-color:{color_dict['header']};")
        elif element_class == 'skipping':
            add_style(element, f"background-color:{color_dict['skipping']};")
        elif element_class == 'section_text':
            add_style(element, f"background-color:{color_dict['section_text']};")
    