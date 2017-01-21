import xml.etree.ElementTree as ET
#conf_file = 'tConfig.sleepDuration.xml'

def find_time(conf_file):
    tree = ET.parse(conf_file)
    root = tree.getroot()
    #print root.attrib
    #print root.tag
    #print 'time:',root[0][0].text
    return root[0][0].text

def findPath(file_name):
    tree = ET.parse(file_name)
    root=tree.getroot()
    return root[0][0].text

#print findPath(conf_file)
