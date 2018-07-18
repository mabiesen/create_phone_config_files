
class TextFile():
    config_lines = []
    json_params = {}

    def __init__(self, filepath, json_params):
        self.json_params = json_params
        with open(filename, "r") as fh:
            self.config_lines = fh.readllines()

    def write_to_file(self, filename, data):
        try:
            for did, d in enumerate(data):
                data[did] = d.replace('\r', '').replace('\n', '')

            with open(filename,'w') as outfile:
                outfile.write("\n".join(data))
        except Exception as e:
            return e, "writing to text file"

    def replace_a_string(self,key,value):
        delimiter = self.json_params["delimiter"]
        ctr = 0
        try:
            for line_id,line in enumerate(self.config_lines):
                if key in line:
                    ctr = ctr + 1
                    self.config_lines[line_id] = self.replace_after_char(line,value,delimiter)
        except Exception as e:
            return e, "replacing in text file"


    def replace_after_char(origstring, addstring, thischar="="):
        if thischar in origstring:
            return origstring.split(thischar, 1)[0] + thischar + addstring
