
class TextFile():
    config_lines = []
    json_params = {}

    def __init__(self, filepath, json_params):
        self.json_params = json_params
        with open(filepath, "r") as fh:
            self.config_lines = fh.readlines()

    # should return true or false depending on success
    def write_to_file(self, filename):
        try:
            # remove newlines to make uniform, may have come from windows
            for did, d in enumerate(self.config_lines):
                self.config_lines[did] = d.replace('\r', '').replace('\n', '')

            with open(filename,'w') as outfile:
                outfile.write("\n".join(self.config_lines))
            return True
        except Exception as e:
            return False

    # should return a count, number of replacements, key
    # error alerts to user should happen in main program
    # the reason:  we want to kill the program if problems, but we
    # dont want to import sys all over the place to kill the program
    def replace_a_string(self,key,value):
        ctr = 0
        try:
            for line_id,line in enumerate(self.config_lines):
                if key in line:
                    ctr = ctr + 1
                    self.config_lines[line_id] = self.replace_after_char(line,value)
            return True, ctr, key
        except Exception as e:
            print(e)
            return False, ctr, key


    def replace_after_char(self,origstring, addstring):
        thischar = self.json_params["text_delimiter"]
        if thischar in origstring:
            return origstring.split(thischar, 1)[0] + thischar + addstring
        if self.json_params["text_delimiter_override"].upper() == "TRUE":
            print("The delimiter was not found, but an override has been set.")
            print("Appending delimiter and value to string")
            return origstring + thischar + addstring
        else:
            print("You have an issue with your selected delimiter! Not found")
            print("The string being evaluated was %s" %(origstring))
            raise ValueError
