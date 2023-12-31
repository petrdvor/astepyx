import re
from pprint import pprint


class TextToDict:
    """Reads lines of text and parses it to nested dict/list according to number of indents
    """

    def __init__(self, indented_line):
        self.sub_element = []
        self.depth = len(indented_line) - len(indented_line.lstrip())
        self.text = indented_line.strip()

    def add_subelement(self, elements):
        sub_el_level = elements[0].depth
        while elements:
            element = elements.pop(0)
            if element.depth == sub_el_level:
                self.sub_element.append(element)
            elif element.depth > sub_el_level:
                elements.insert(0,element)
                self.sub_element[-1].add_subelement(elements)
            elif element.depth <= self.depth:
                elements.insert(0,element)
                return

    def export_to_dict(self):
        if len(self.sub_element) > 1:
            return {self.text: [sub_el.export_to_dict() for sub_el in self.sub_element]}
        elif len(self.sub_element) == 1:
            return {self.text: self.sub_element[0].export_to_dict()}
        else:
            return self.text

class AsterixSpecification:
    def __init__(self, spec_file) -> None:

        with open(spec_file) as f:
            lines = [line.rstrip() for line in f]

        main_doc = TextToDict('doc')
        main_doc.add_subelement([TextToDict(line) for line in lines if line.strip()])
        d = main_doc.export_to_dict()['doc']

        self.spec_dict = {}
        self.specification = {}

        for block in d:
            for k, v in block.items():
                self.spec_dict[k]=v

        self.items = {}
        for item_spec in self.spec_dict['ast']:
            item = self.parse_item(item_spec)
            self.items.update({item['id']:item})

        self.uap = self.spec_dict['uap']
        self.uap = [u if u!='null' else None for u in self.uap]  # nulls to None

        self.specification.update({'ast':self.items})
        self.specification.update({'uap':self.uap})

        # Yaml output, if necessary
        # import yaml
        # yaml_output = yaml.dump(self.items, sort_keys=False)
        # print(yaml_output)

    def parse_item(self, item_spec):
        """Parses item from raw specification in txt files to dict structure

        Args:
            item_spec (dict): Raw item specification
                              Eg.:
                                {'010': [{'title': 'Data Source Identification'},
                                        {'format': 'fixed'},
                                        {'length': '2'},
                                        {'elements': ['16 9 "System Area Code" "SAC"',
                                                    '8 1 "System Identification Code" "SIC"']}]}

        Returns:
            dict: Parsed ASTERIX Item
                  Eg.
                    {'id': '010',
                     'title': 'Data Source Identification',
                     'format': 'fixed',
                     'length': 2,
                     'elements': [{'from': 16, 'to': 9, 'name': 'System Area Code', 'short_name': 'SAC'},
                                  {'from':  8, 'to': 1, 'name': 'System Identification Code', 'short_name': 'SIC'}
                                 ]
                    }
        """

        item = {}

        item['id'] = list(item_spec.keys())[0]  # read the key = item id

        for subitem in list(item_spec.values())[0]:  # subitem = title|format|length|elements...

            subitem_key = list(subitem.keys())[0]
            subitem_val = list(subitem.values())[0]

            if subitem_key == 'title':
                item['title'] = subitem_val
            if subitem_key == 'format':
                item['format'] = subitem_val
            if subitem_key == 'length':
                item['length'] = int(subitem_val)
            if subitem_key == 'elements':
                item['elements'] = self.parse_elements(subitem_val)
            if subitem_key == 'octets':
                if 'length' in item:
                    item['octets'] = self.parse_octets(subitem_val, item['length'])
                else:
                    item['octets'] = self.parse_octets(subitem_val)
            if subitem_key == 'subitems':
                item['subitems'] = self.parse_subitems(subitem_val)
        # pprint(item, sort_dicts=False)
        return item

    def parse_subitems(self, subitems_raw):
        """Browses compound subitems and parses them.

        Args:
            subfields (list(dict)): List of raw subitems of compound item.
                                    Eg.:
                                    [{'ADR': [{'title': '24 bits Target Address'},
                                            {'format': 'fixed'},
                                            {'length': '3'},
                                            {'elements': '24 1 "Target Address" "ADR"'}]},
                                    {'ID': [{'title': 'Target Identification'},
                                            {'format': 'fixed'},
                                            {'length': '6'},
                                            {'elements': {'48 1 "Target Identification" "TID"': {'encode': '6bitchar'}}}
                                            ]
                                    },...]

        Returns:
            list(dict): Lsit of dicts of parsed subitems.
        """
        subitems_parsed = []
        for si in subitems_raw:
            subitems_parsed.append(self.parse_item(si))
        return subitems_parsed

    def parse_octets(self, octets, *args):
        """Parses octets of variable length ASTERIX items.

        Args:
            octets (list(dicts)): List of raw octets, as read from txt file
            args: number of bytes in subparts if other than 1 (because of I062/510)

        Returns:
            _type_: _description_
        """
        if args:
            length = args[0]
        else:
            length = 1

        if isinstance(octets, dict):
            octets = [octets]
        octets_parsed = []
        for octet in octets:
            elements = self.parse_elements(octet['elements'])

            octets_parsed.append({'elements':elements, 'length':length})
        return octets_parsed

    def parse_elements(self, elements):
        elements_decoded = []

        if isinstance(elements, list):
            for el in elements:
                elements_decoded.append(self.parse_element(el))
        else:
            elements_decoded.append(self.parse_element(elements))
        return elements_decoded

    def parse_element(self, element_spec):
        if isinstance(element_spec, str):
            element = self.parse_element_line(element_spec)
            return element
        elif isinstance(element_spec, dict):
            element = self.parse_element_dict(element_spec)
            return element
        else:
            print('ERROR DECONDIG ELEMENTS')

    def parse_element_dict(self, element_dict):
        el_line = list(element_dict.keys())[0]
        element = self.parse_element_line(el_line)
        el_vals = list(element_dict.values())[0]

        if isinstance(el_vals, dict):
            el_vals = [el_vals]

        for element_params in el_vals:
            if 'encode' in element_params:
                element['encode'] = element_params['encode']
            if 'scale' in element_params:
                element['scale'] = float(eval(element_params['scale']))
        return element

    def parse_element_line(self, element_line):
        # print(element_line)
        element = {}
        e = element_line.split(' ')
        element['from'] = int(e[0])
        element['to'] = int(e[1])
        names_indices = [m.start() for m in re.finditer('"',element_line)]
        element['name'] = element_line[names_indices[0]+1:names_indices[1]]
        element['short_name'] = element_line[names_indices[2]+1:names_indices[3]]
        return element

if __name__ == '__main__':
    aso = AsterixSpecification('specs/ast_spec_cat034_ed1.29.txt')