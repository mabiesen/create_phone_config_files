from xml.dom import minidom

def parse_xml(xml):
    xmldoc = minidom.parse(xml)
    return xmldoc.getElementsByTagName('car')[2].firstChild.nodeValue
