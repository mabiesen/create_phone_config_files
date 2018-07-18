# class to represent both xml and text Files
# this will allow for singularity in code, reduction of if startements
# this also makes sense give that we have constantly changing data structure
#(i.e.  better than returning and creating new var everyt time)

from util_text_file import TextFile
from util_xml_file import XMLFile


class ProvisionFiles():

    json_params = {}
    mytool = ""


    def __init__(self, config_filepath, json_params):
        self.json_params = json_params

        # store json params in the instance variable
        # call the json params from within as part of self
        if json_params["textOrXML"] == "text":
            self.mytool = TextFile(filepath, json_params)
        else:
            self.mytool = XMLFile(filepath, json_params)


    def write_to_file(self, filepath, data):
        self.mytool.write_to_file(filepath, data)

    def replace_a_string():
        self.mytool.replace_a_string()
