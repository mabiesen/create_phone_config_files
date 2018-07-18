from util_xml import *

x = xmlwrapper("thisfile.xml")

x.replace_tag_text("car","butt")

x.write_to_file("output.xml")
