from time import sleep

import requests
from bs4 import BeautifulSoup


def scrape_one_page(url):
    """Scrape one page of startupnationcentral.com and return a list of links to articles."""


    # Get the page
    page = requests.get(url)

    # Parse the page
    soup = BeautifulSoup(page.text, 'html.parser')

    # Get the divs with class 'company'
    company_divs = soup.find_all('div', class_='company')

    companies = []
    for div in company_divs:
        cols = div.find_all(class_='table-row-item')
        if (len(cols)>0):
            company = {
                'Name':         my_strip(cols[0].text),
                'Description':  my_strip(cols[1].text),
                'Founded':      my_strip(cols[2].text),
                'BizModel':     my_strip(cols[3].text),
                'Employees':    my_strip(cols[4].text),
                'Stage':        my_strip(cols[5].text),
                'Raised':       my_strip(cols[6].text),
                'Sectors':      my_strip(cols[7].text)
            }
            companies.append(company)

    return companies


def my_strip(str):
    return '"' + str.replace('\n', ' ').replace('"', '\\"').replace('\r', '').strip() + '"'


page_num = 1
if __name__ == "__main__":
    #
    companies = []

    for page_num in range(1, 1000):
        # sleep(10)
        print ("Scraping page " + str(page_num))
        res = scrape_one_page(
            # 'https://finder.startupnationcentral.org/company/search?sort=fundingstages-asc&sectorclassification=agxzfmlsbGlzdHNpdGVyJAsSF0Jhc2VDbGFzc2lmaWNhdGlvbk1vZGVsGICA4Jvz2KAJDA&status=Active&page=1');
            'https://finder.startupnationcentral.org/company/search?page='+str(page_num))
        if len(res) == 0 or page_num >2:
            file_str = ''
            file_str = ','.join(companies[0].keys()) + '\n'
            for company in companies:
                file_str += ','.join(company.values()) + '\n'
            with open('companies.csv', 'w') as f:
                f.write(file_str)
            break

        else :
            companies += res



