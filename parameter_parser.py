import wpilib
from xml.etree import ElementTree

class Parameters:
    XML_FILE = '/parameters.xml'
    def __init__(self):
        self.root = None
        self.load_xml()

    def load_xml(self, xml_file=None):
        if xml_file is None:
            xml_file = self.XML_FILE
        self.root = ElementTree.parse(xml_file)

    def get_element
