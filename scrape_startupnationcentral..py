from lxml import html

import sys


filename = '/Users/hed-bar-nissan/Downloads/Energy_sector'


with open(filename, 'r') as myfile:
    page = myfile.read()
    tree = html.fromstring(page)

    elements = tree.xpath('//div[@class="title"]')
    for i,elem in enumerate(elements):
        print (str(i) + " : " + elem.text + " : " + elem.getparent().getchildren()[1].text)

