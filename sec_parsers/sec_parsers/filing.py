from lxml import etree
from sec_parsers.parsers_helper import parse_metadata, detect_filing_type, setup_html
from sec_parsers.parsers import SEC_10K_Parser, SEC_10Q_Parser, SEC_8K_Parser, SEC_S1_Parser, SEC_20F_Parser
import csv
import unicodedata


class Filing:
    def __init__(self, html):
        self.metadata = {}
        self._setup_html(html)
        self._parse_metadata()
        self.hierarchy = None # need to implement
        self.xml = None
        self.parser = None # this will be updated by detect_filing_type
        self.filing_type = None
        self._detect_filing_type()
        self._update_parser()


    # keep
    def _setup_html(self,html):
        if type(html).__name__ == 'SEC_Download': # incorporate download metadata
            self.metadata = html.metadata
        self.html = setup_html(html)

    # keep
    def _parse_metadata(self):
        metadata_from_xbrl = parse_metadata(self.html)
        self.metadata.update(metadata_from_xbrl)

    # keep
    def _detect_filing_type(self):
        filing_type = detect_filing_type(self.metadata)
        self.filing_type = filing_type

    def _update_parser(self):
        if self.filing_type is None:
            self._detect_filing_type()
        filing_type = self.filing_type

        if filing_type == '10-K':
            self.parser = SEC_10K_Parser()
        elif filing_type == '10-Q':
            self.parser = SEC_10Q_Parser()
        elif filing_type == '8-K':
            self.parser = SEC_8K_Parser()
        elif filing_type == 'S-1':
            self.parser = SEC_S1_Parser()
        elif filing_type == '20-F':
            self.parser = SEC_20F_Parser()


    # keep
    def set_filing_type(self, filing_type):
        self.filing_type = filing_type
        self._update_parser()

    def parse(self,add_parsing_id=False):
        if self.filing_type is None:
            self._detect_filing_type()

        self.parser.iterative_parse(self.html,add_parsing_id)
        self.parser.clean_parse(self.html)
        # convert to xml
        self._to_xml(add_parsing_id)

    def visualize(self):
        self.parser.visualize(self.html)

    def _to_xml(self,add_parsing_id=False):
        self.xml = self.parser.construct_xml_tree(html=self.html,metadata=self.metadata,add_parsing_id=add_parsing_id)


    # functions to interact with xml

    # Find #
    def find_all_sections_from_title(self,title):
        title = title.strip().lower()
        if self.xml is None:
            self.to_xml()

        # select all nodes with title attribute
        titles = self.xml.xpath(f"//*[@title]")
        # find all nodes with title
        nodes = [node for node in titles if title in node.attrib['title'].lower()]

        return nodes
    
    def find_section_from_title(self,title):
        sections = self.find_all_sections_from_title(title)
        return sections[0] if sections else None

    def find_all_sections_from_text(self, text):
        """Find a node by text."""
        if self.xml is None:
            self.to_xml()

        return self.xml.xpath(f"//*[contains(text(), '{text}')]")
    
    def find_section_from_text(self, text):
        sections = self.find_all_sections_from_text(text)
        return sections[0] if sections else None
    
    # Interact with Node #
    def get_subsections_from_section(self, node):
        """Get all children of a node."""
        return node.getchildren()
    
    def get_nested_subsections_from_section(self, node):
        """Get all children of a node, including nested children."""
        return list(node.iterdescendants())

    # Note, needs refactor, also needs better spacing fix with text.
    def get_text_from_section(self, node, include_title=False):
        """Gets all text from a node, including title string for child nodes."""
        text = ''

        # Add title for child nodes only
        if include_title:
            text += node.attrib.get('title', '') + '\n'

        node_text = node.text
        if node_text is not None:
            text += node.text + '\n'
        
        for child in node:
            # Pass False to indicate this is a child node
            text += self.get_text_from_section(child, include_title=True)
        
        return text
    
    # Interact with tree #

    # TODO: user friendly - e.g. if parsed not called call parse
    def get_tree(self,node=None, level=0):
        if node is None:
            node = self.xml
        tree_string = node.tag
        for child in node:
            tree_string += '\n' + '|-' * level + self.get_tree(child, level + 1)
        return tree_string
    
    def get_title_tree(self,node=None,level=0,attribute='title'):
        if node is None:
            node = self.xml
        elif node.tag == 'metadata':
            return   "Metadata"

            
        tree_atrib = node.attrib.get(attribute,'')
        if 'signatures' in tree_atrib.lower(): #workaround for adding signatures section but not signature parsing
            pass
        else:
            for child in node:
                tree_atrib += '\n' + '|-' * level + self.get_title_tree(child, level + 1,attribute)

        return tree_atrib
    
    # Save to file #
    def save_xml(self, filename, encoding='utf-8'):
        if encoding not in ['utf-8','ascii']:
            raise ValueError('Encoding must be either utf-8 or ascii')
        
        if self.xml is None:
            self.to_xml()

        if encoding == 'ascii':
            self.convert_element_to_ascii(self.xml)

        with open(filename, 'wb') as f:
                f.write(etree.tostring(self.xml,encoding=encoding,xml_declaration=True))

            
    def save_csv(self, filename, encoding='utf-8'):
        if encoding not in ['utf-8','ascii']:
            raise ValueError('Encoding must be either utf-8 or ascii')
        
        if encoding == 'ascii':
            self.convert_element_to_ascii(self.xml)
        
        def get_rows(node,path):
            path = path + "/" + node.attrib.get('title')

            row_list = []

            row = {}
            row['path'] = path
            row['text'] = self.get_text_from_section(node)
            row_list.append(row)
            for child in node:
                row_list.extend(get_rows(child,path))

            return row_list
        
        row_list = []
        for child in self.xml.getchildren():
            row_list.extend(get_rows(child,''))
        
        keys = row_list[0].keys()

        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(row_list)
            
    def save_html(self, filename):
        # Assuming you have an lxml object called 'tree'
        html_string = etree.tostring(self.html, pretty_print=True, method="html")

        # Save the HTML to a file
        with open(filename, "wb") as file:
            file.write(html_string)

    # TODO: implement
    def save_dta(self, filename):
        pass

    # encoding
    # Function to convert text to ASCII
    def string_to_ascii(self, string):
        # Normalize to closest ASCII equivalent
        normalized = unicodedata.normalize('NFKD', string)
        # Remove non-ASCII characters
        ascii_string = normalized.encode('ascii', 'ignore').decode('ascii')
        return ascii_string

    # Recursively process all elements and their text
    def convert_element_to_ascii(self,element):
        if element.text:
            element.text = self.string_to_ascii(element.text)
        for child in element:
            self.convert_element_to_ascii(child)
        if element.tail:
            element.tail = self.string_to_ascii(element.tail)
    

        
