from lxml import html
import requests
import time
import os
import codecs

def santize_for_filename(input):
  input = input.replace('/','_')
  return input

os.chdir('C:/Users/hedbn/PycharmProjects/misc/gartner_scraping/')

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'})

page =''
# r = s.get('https://www.gartner.com/en/research/magic-quadrant')
# page = r.content

# print(r.headers)
# print( r.request.headers)
#time.sleep(3)


  with open('Magic Quadrants Research Methodologies-14_6_19.html', 'r') as myfile:
    page = myfile.read()



  tree = html.fromstring(page)


publications_elems = tree.xpath('//table[@class="publication-table"]//a')

publications = []
for elem in publications_elems:
  obj = {'name': elem.text, 'href': elem.attrib['href']}
  obj['name'] = santize_for_filename(obj['name'])

  if (obj['href'][0] == '#'
          # or obj['name'][0] < 'E'
  ):
    continue
  publications.append(obj)

  # print (obj)
  # page = s.get(obj['href']).text
  # file = codecs.open(obj['name'] + '.html', "w","utf-8")
  # file.write(page)
  # file.close()
  # time.sleep(3)


vendors = {}

for p in publications:
  # print (p['name'])
  p['vendors'] = []
  # file = codecs.open(p['name'] + '.html','r',"utf-8")
  file = codecs.open(p['name'] + '.html','r')
  try:
    tree = html.fromstring(file.read())
  except:
    print ("Problem with decoding " + p['name'])
    continue

  lis = tree.xpath('//li')
  for li in lis:
    if li.text is not None \
            and li.text.startswith('Vendor')\
            and li.text !='Vendors Added and Dropped':
      # print ('\t' + li.text)
      lis1 = li.xpath('.//li')
      for li1 in lis1:
        if li1.text is not None and li1.text.strip()!='':
          # print('\t\t' + li1.text)
          vendor_name = li1.text
          p['vendors'].append(vendor_name)
          if vendor_name in vendors:
            vendors[vendor_name] += 1
          else:
            vendors[vendor_name] = 1

for k in vendors.keys():
  print(k,'\t',vendors[k])






