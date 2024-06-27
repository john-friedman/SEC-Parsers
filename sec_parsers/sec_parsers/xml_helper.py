# Note, we'll be using 'node' for xml and 'element' for html terminology
# Note: adding helpers for tree / root / node, so easier for less technical people
import xml.etree.ElementTree as ET

# lazy so used chatgpt for this
def is_tree(tree):
    """
    Check if the given object is a valid ElementTree instance.

    Parameters:
    tree (ET.ElementTree): The XML tree to check.

    Returns:
    bool: True if the object is a valid ElementTree, False otherwise.
    """
    try:
        # Try to get the root element of the tree
        root = tree.getroot()
        return True
    except AttributeError:
        # The tree object doesn't have a getroot method
        return False
    except ET.ParseError:
        # The tree object is not properly parsed
        return False



def print_xml_structure(node):
    if is_tree(tree):
        root = tree.getroot()

    def indent(level):
      return "|--" * level

    def print_element(element, level):
      print(indent(level) + element.tag)
      for child in element:
        print_element(child, level + 1)

    print_element(node, 0)


def get_text_from_node(node):
    text = ''
    if node.text is not None:
        text = node.text.strip()
    for child in node:
        text += get_text_from_node(child)
    
    return text

def save_xml(tree, file_path):
    if not is_tree(tree):
      tree = ET.ElementTree(tree)
    tree.write(file_path, encoding='utf-8-sig', xml_declaration=True)