from pathlib import Path
from bs4 import BeautifulSoup
import codecs



def iterate_html_forms(dir_path):
    pathlist = Path(dir_path).glob('**/*.htm*')
    for path in pathlist:
        f = codecs.open(path, encoding='utf-8')
        # print("reading "+ str(path))
        html_str = f.read()
        doc = BeautifulSoup(html_str , 'html.parser')
        forms = doc.findAll('form')
        for form in forms:
            yield str(form)


i:int = 0
for form in iterate_html_forms('C:/Users/hedbn/Documents/site_corpus'):
    print (i)
    i+=1




# rows = bs_table.find_all('tr')
# for row in rows:
#     cells = row.find_all(['td', 'th'])
#     for cell in cells:
#         print(cell.name, cell.attrs)