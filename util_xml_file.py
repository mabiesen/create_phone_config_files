from xml.etree import ElementTree as et

class XMLFile():

    working_tree=""

    def __init__ (self,xmlfilepath):
        self.working_tree = et.parse(xmlfilepath)

    def replace_a_string(self,tag,newtext):
        try:
            for item in self.working_tree.iter(tag):
                item.text = newtext
        except Exception as e:
            return e, "replacing in xml"

    def write_to_file(self,xmlfilepath):
        try:
            self.working_tree.write(xmlfilepath)
        except Exception as e:
            return e, "writing to xml file"
