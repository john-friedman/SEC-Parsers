from lxml import etree as ET


# Functions that are useful for the user
# e.g. find all elements with a certain text

# think about style, how to differentiate user functions versus helper functions (e.g. _get_all_text)

# search if node contains text
def find_by_text(node, text):
    """Find a node by text."""
    return node.xpath(f"//*[contains(text(), '{text}')]")

# get all text from node
# includes desc
def get_node_text():
    pass

def find_node_by_title():
    pass

def find_node_by_desc():
    pass

def save_xml():
    pass

def get_node_tree(node, level=0):
    tree_string = node.tag
    for child in node:
        tree_string += '\n' + '|-' * level + get_node_tree(child, level + 1)
    return tree_string

def get_node_attributes(node,level=0,attribute='title'):
    tree_atrib = node.attrib.get(attribute,'')
    for child in node:
        tree_atrib += '\n' + '|-' * level + get_node_attributes(child, level + 1,attribute)

    return tree_atrib