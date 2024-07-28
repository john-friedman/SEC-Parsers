from sec_parsers.string_detector_groups import HeaderStringDetectorGroup, SEC_10K_StringDetectorGroup, SEC_8K_StringDetectorGroup, SEC_S1_StringDetectorGroup
from sec_parsers.xml_helper import get_text, get_all_text,\
        set_background_color, remove_background_color, open_tree, is_middle_element
from sec_parsers.cleaning import clean_title
from sec_parsers.visualization_helper import headers_colors_list
from lxml import etree

from sec_parsers.element_detector_groups import HeaderElementDetectorGroup, SEC_10K_ElementGroup, SEC_8K_ElementGroup

# TODO: refactor to reduce code duplication / annoying stuff like detectors all over the place

# TODO, probably add autosort later
class HTMLParser:
    def __init__(self, **kwargs):
        self.element_detector_group = HeaderElementDetectorGroup() # parses elements
        self.string_detector_group = HeaderStringDetectorGroup() # parses strings
        self.color_dict = {'remove;': '#f2f2f2','skip;':'#FAFAD2'} # If you want certain parsing types to have certain colors

        self._init(**kwargs)
        self.all_detectors = self.element_detector_group.element_detectors + self.string_detector_group.string_detectors
        self.sort_detectors()

    def _init(self, **kwargs):
        # This method is meant to be overridden by subclasses
        pass

    def sort_detectors(self):
        """sorts detector by parsing rule. Return first"""

        # Separate detectors into 'return' and 'continue' groups
        return_detectors = [detector for detector in self.all_detectors if detector.parsing_rule == "return"]
        continue_detectors = [detector for detector in self.all_detectors if detector.parsing_rule == "continue"]

        # Combine the groups, with 'return' detectors first
        self.all_detectors = return_detectors + continue_detectors


    def detect_style_from_string(self,string,rule_list=[]):
        string_detectors = self.string_detector_group.string_detectors
        # subset
        if rule_list: # WIP
            string_detectors = [detector for detector in string_detectors if detector.parsing_rule in rule_list]
        
        result = ''
        for detector in string_detectors:
            string_style = detector.detect(string)
            if string_style != '':
                parsing_rule = detector.parsing_rule
                if parsing_rule == 'return':
                    return string_style, parsing_rule
                else:
                    result += string_style
        
        return (result,'continue')
    
    
    def detect_style_from_element(self,element,rule_list=[]):
        element_detectors = self.element_detector_group.element_detectors
        # subset
        if rule_list: # WIP
            element_detectors = [detector for detector in element_detectors if detector.parsing_rule in rule_list]
        
        result = ''
        for detector in element_detectors:
            element_style = detector.detect(element)
            if element_style != '':
                parsing_rule = detector.parsing_rule
                if parsing_rule == 'return':
                    return element_style, parsing_rule
                else:
                    result += element_style
        
        return (result,'continue')
    
    # possible performance increases - move which detector triggers first
    def iterative_parse(self,html,add_parsing_id=False):
        count = 0

        flag = True
        orig_elem = None
        element_style = ''
        string_style = ''
        parser = self
        # add xml construction later?
        for event, elem in etree.iterwalk(html, events=('start', 'end')): # fast, .7s
            if event == 'start':
                if add_parsing_id:
                    elem.attrib['parsing_id'] = str(count)
                    count += 1  
                    
                if flag:
                    # refactor to seperate function
                    result, parsing_rule = parser.detect_style_from_element(elem)
                    if parsing_rule == 'return':
                        element_style = result
                        orig_elem = elem
                        flag = False
                        continue
                    elif result != '':
                        if orig_elem is None:
                            orig_elem = elem

                        element_style += result

                    if string_style == '':
                        string = get_all_text(elem)
                        result, parsing_rule = parser.detect_style_from_string(string)
                        if parsing_rule == 'return':
                            string_style = result
                            orig_elem = elem
                            flag = False
                            continue
                        elif result != '':
                            if orig_elem is None:
                                orig_elem = elem

                            string_style += result

                    # code to check if elem is in middle 
                    if (element_style + string_style) != '':
    
                        if is_middle_element(orig_elem):
                            element_style =''
                            string_style = ''
                            orig_elem = None

                else:
                    pass # iterate through file without parsing

            elif event == 'end':
                if orig_elem is not None:
                    if elem == orig_elem:
                        parsing_string = element_style + string_style
                        orig_elem.attrib['parsing_string'] = parsing_string

                        flag = True
                        orig_elem = None
                        string_style = ''
                        element_style = ''

    # Works
    def clean_parse(self,html):
        """set ignore items etc"""
        parsed_elements_to_pop = html.xpath("//*[@parsing_string='']") # should be able to delete this now
        for element in parsed_elements_to_pop:
            element.attrib.pop('parsing_string', None)

        parsed_elements = html.xpath('//*[@parsing_string]')

        # figure out how to manage remove, skip, and header strigns here
        remove_strings = [item.style for item in self.all_detectors if item.cleaning_rule == 'remove;']
        skip_strings = [item.style for item in self.all_detectors if item.cleaning_rule == 'skip;']
        for parsed_element in parsed_elements:
            parsing_string = parsed_element.get('parsing_string')  

            parsing_list = parsing_string.split(';') 
            parsing_list = [parsing for parsing in parsing_list if parsing != '']
            parsing_list = [parsing +';' for parsing in parsing_list]

            # check if ignore
            if any([parsing in remove_strings for parsing in parsing_list]):
                parsed_element.attrib['parsing_type'] = 'remove;'
                #parsed_element.attrib['parsing_log'] += 'clean-parse-ignored;'
            # check if text
            elif any([parsing in skip_strings for parsing in parsing_list]):
                parsed_element.attrib['parsing_type'] = 'skip;'
                #parsed_element.attrib['parsing_log'] += 'clean-parse-text;'
            else:
                parsed_element.attrib['parsing_type'] = parsing_string
                #parsed_element.attrib['parsing_log'] += 'clean-parse-header;'


    # works
    def visualize(self,html):
        # remove style from all descendants so that background color can be set
        for descendant in html.iterdescendants():
            remove_background_color(descendant)

        # find all elements with parsing attribute
        elements = html.xpath('//*[@parsing_type]')
        # get all unique parsing values
        parsing_values = list(set([element.attrib['parsing_type'] for element in elements]))
        color_dict =dict(zip(parsing_values, headers_colors_list[:len(parsing_values)]))
        color_dict.update(self.color_dict)
        # we want header scale, ignore color

        for element in elements:
            # get attribute parsing
            parsing = element.attrib['parsing_type']
            if parsing == '':
                pass
            else:
                color = color_dict[parsing]
                set_background_color(element, color)

        open_tree(html)

    # should be fixed
    def construct_xml_tree(self, html, metadata, add_parsing_id=False):
        root = etree.Element('root')
        document_node = etree.Element('document', title='Document')
        document_node.attrib['parsing_type'] = 'added in tree construction;'
        root.append(document_node)

        levels_dict = {item.style: item.level for item in self.all_detectors if item.level != -1}
        base_headers = [key for key in levels_dict.keys() if levels_dict[key] == 0]


        # ELEMS TO REMEMBER UNTIL NEXT HEADER
        last_section_text = ''
        last_section_title = ''
        last_section_elem = None
        last_section_parsing_type = ''
        last_section_tag = 'introduction'

        # Defining for introduction special case
        last_section_text = ''
        last_section_title = 'introduction'
        last_section_parsing_type = 'introduction;'
        last_section_tag = 'introduction'

        stack = [document_node]  # added to until header, then modified
        level = None

        flag = True
        remove_elem = None
        for current_event, current_elem in etree.iterwalk(html, events=('start', 'end')): # change to iterwalk to skip certain elements
            if current_event == 'start':

                if remove_elem is not None:
                    continue

                if last_section_elem is not None:
                    if add_parsing_id:
                        node.attrib['parsing_id'] = last_section_elem.attrib['parsing_id']
                    continue

                current_parsing_type = current_elem.attrib.get('parsing_type', '')

                if current_parsing_type == 'remove;': # WIP
                    remove_elem = current_elem
                    continue

                if flag: # handle introduction
                    if current_parsing_type in base_headers:
                        flag = False

                        # initialize node using last_section
                        node = etree.Element(last_section_tag, title=last_section_title)
                        node.text = last_section_text
                        node.attrib['parsing_type'] = last_section_parsing_type
  

                        # handle where to append to
                        # append node to document
                        document_node.append(node)
                        # append node to stack
                        stack.append(node)

                        # reset last_section
                        last_section_text = ''
                        last_section_title = clean_title(get_all_text(current_elem))
                        last_section_elem = current_elem
                        last_section_parsing_type = current_parsing_type

                        if current_parsing_type in [key for key in levels_dict.keys()]:
                            level = levels_dict[current_parsing_type]
                            last_section_tag = last_section_parsing_type.replace(';', '')
                        else:
                            level = None
                            last_section_tag = 'company_designated_header'
                    else:
                        last_section_text += get_text(current_elem)
                else:
                    if current_parsing_type == 'skip;':
                        last_section_text += get_text(current_elem)
                    elif current_parsing_type == '':
                        last_section_text += get_text(current_elem)
                    else:
                        # initialize node using last_section
                        node = etree.Element(last_section_tag, title=last_section_title)
                        node.text = last_section_text
                        node.attrib['parsing_type'] = last_section_parsing_type

                        # handle where to append to
                        if level is not None: # WIP
                            parent_node = stack[level]
                            stack = stack[:level+1]

                            parent_node.append(node)
                            stack.append(node)

                        else:
                            parsing_type_list = [item.attrib['parsing_type'] for item in stack]
                            if last_section_parsing_type in parsing_type_list:
                                idx = parsing_type_list.index(last_section_parsing_type)
                                
                                if idx == len(stack) - 1:  # If it's the last element
                                    stack[idx-1].append(node)
                                    stack = stack[:idx]  # Remove the last element
                                    stack.append(node)  # Replace with the new node
                                else:
                                    stack = stack[:idx+1]
                                    stack[idx].append(node)
                                    stack.append(node)
                            else:
                                stack[-1].append(node)
                                stack.append(node)

                        # reset last_section
                        last_section_text = ''
                        last_section_title = clean_title(get_all_text(current_elem))
                        last_section_elem = current_elem
                        last_section_parsing_type = current_parsing_type

                        if current_parsing_type in [key for key in levels_dict.keys()]:
                            level = levels_dict[current_parsing_type]
                            last_section_tag = last_section_parsing_type.replace(';', '')
                        else:
                            level = None
                            last_section_tag = 'company_designated_header'
            else:
                if current_elem == remove_elem:
                    remove_elem = None
                    continue

                if current_elem == last_section_elem:
                    last_section_elem = None
                    continue

        # add metadata
        metadata_node = etree.Element('metadata')
        for key in metadata.keys():
            node = etree.Element(key) 
            node.text = str(metadata[key])
            metadata_node.append(node)
        # insert metadata at beginning
        root.insert(0,metadata_node)


        return root

        
# WIP FIX numbers inside pagraphs sometimes parsing as page numbers
class SEC_10K_Parser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)  # Call the parent's _init method

        self.element_detector_group = SEC_10K_ElementGroup()
        self.string_detector_group = SEC_10K_StringDetectorGroup()

        self.color_dict.update({'part;': '#B8860B',
                       'item;': '#BDB76B',
                       'bullet point;': '#FAFAD2',
                          'signatures;': '#B8860B',
                       })


# 10Q and 10K are the same for now
class SEC_10Q_Parser(SEC_10K_Parser):
    pass

class SEC_8K_Parser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)

        self.element_detector_group = SEC_8K_ElementGroup()
        self.string_detector_group = SEC_8K_StringDetectorGroup()
        self.color_dict.update({
                       'item;': '#B8860B',
                       'bullet point;': '#FAFAD2',
                          'signatures;': '#B8860B',
                       })
        
class SEC_S1_Parser(HTMLParser):
    def _init(self, **kwargs):
        super()._init(**kwargs)

        self.element_detector_group = SEC_10K_ElementGroup()
        self.string_detector_group = SEC_S1_StringDetectorGroup()


        self.color_dict.update({
                       'prospectus;': '#B8860B',
                       'item;': '#BDB76B',
                       'signatures;': '#B8860B',
                       'bullet point;': '#FAFAD2',
                       })
        
class SEC_20F_Parser(SEC_10K_Parser):
    pass