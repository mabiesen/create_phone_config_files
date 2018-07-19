from xml.etree import ElementTree as et

class XMLFile():

    json_params = {}
    working_tree=""

    def __init__ (self,xmlfilepath, json_params):
        self.working_tree = et.parse(xmlfilepath)
        self.json_params = json_params

    # should return success or failure
    def write_to_file(self,xmlfilepath):
        try:
            self.working_tree.write(xmlfilepath)
            return True
        except Exception as e:
            return False

    # should return a count, number of replacements, key
    # error alerts to user should happen in main program
    # the reason:  we want to kill the program if problems, but we
    # dont want to import sys all over the place to kill the program
    def replace_a_string(self,key,value):
        try:
            ctr = 0
            for item in self.working_tree.iter(key):
                item.text = value
                ctr = ctr + 1
            return True, ctr, key
        except Exception as e:
            return False, ctr, key
