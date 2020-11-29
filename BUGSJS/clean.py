from lxml import etree
import sys

file_path = sys.argv[1]
root = etree.parse(file_path)
for element in root.iterfind('.//testsuite'):
    if(element.find('.//testcase')) is None:
        element.getparent().remove(element)

root.write(file_path, pretty_print=True, xml_declaration=True, encoding="utf-8")