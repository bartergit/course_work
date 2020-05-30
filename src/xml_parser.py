import xml.etree.ElementTree as ET
from pickle_manip import *
from dictionary import format_sentence


def xml_parse():
    output = []
    for i in range(2, 4070):
        try:
            tree = ET.parse('corpus/opcorpora_xml/{}.xml'.format(i))
            root = tree.getroot()
            for paragraph in root[1]:
                output.append(format_sentence(paragraph[0][0].text))  # text (name) -> paragraphs -> paragraph -> sentence -> source
        except:
            pass
    return output


if __name__ == "__main__":
    save_pickle_obj(xml_parse(), "corpus/xml")
