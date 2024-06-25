
# Note, we'll be using 'node' for xml and 'element' for html terminology

# change to get
def print_xml_structure(tree):
    root = tree.getroot()

    def indent(level):
      return "|--" * level

    def print_element(element, level):
      print(indent(level) + element.tag)
      for child in element:
        print_element(child, level + 1)

    print_element(root, 0)


def get_text_from_node(node):
    text = ''
    if node.text is not None:
        text = node.text.strip()
    for child in node:
        text += extract_text(child)
    
    return text