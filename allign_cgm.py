# write a python script that loads an html file from the file system and extract all the elements with class "daily-detail"
import datetime

from bs4 import BeautifulSoup

with open("/Users/hed-bar-nissan/Downloads/cgm_report_2281155344_10907.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')



table =  soup.find_all('table')[0]
rows = table.findChildren("tr")
rows = iter(rows)

for row in rows:
    if  row.has_attr('class') and 'daily-report-table-row' in row['class']:
        children = row.findChildren("td", {'class' : 'table-row-date'},recursive=False)
        if len(children) > 0:
            date = children[0].text.strip()
            date = date.split(" ")[0]
            # print(date)
        row = next(rows)

        children = row.findChildren("td", {'class' : 'table-row-date'},recursive=False)
        if len(children) > 0:
            date = children[0].text.strip()
            date = date.split(" ")[0]

        for detail in row.findChildren('div', {'class' : 'daily-detail'},recursive=True):
            children = detail.findChildren("span", recursive=False)

            hour = children[0].text
            time1 = datetime.datetime(2023,int(date.split('.')[1]),int(date.split('.')[0]), int(hour.split(':')[0])+2 , int(hour.split(':')[1]) )

            print (time1.strftime('%Y-%m-%d %H:%M:%S'), "\t",children[1].text)


        # print(row)
