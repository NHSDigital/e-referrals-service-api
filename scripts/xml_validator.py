import glob
from lxml import etree

parser = etree.XMLParser()
XML_files = glob.glob("proxies/**/*.xml", recursive=True)

for file in XML_files:
    try:
        etree.parse(file, parser)
    except Exception as e:
        print("XML parsing error on", file, ":")
        print(e)
        exit(1)

print("No XML syntax errors.")
