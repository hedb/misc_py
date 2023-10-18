from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


def add_data_from_internal_page(browser,farm,url):
    browser.get(url)
    time.sleep(2)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h6.host-feature-title")))
    features = browser.find_elements(by=By.CSS_SELECTOR, value="h6.host-feature-title")

    for f in features:
        title = f.text
        # parent = f.find_element_by_xpath("..")
        parent = f.find_elements( by=By.XPATH  ,value = "..")[0]
        values = parent.find_elements(by=By.XPATH,value=".//*[@class='host-feature']")
        value_str = ''
        if len(values) > 0:
            for v in values:
                icons = v.find_elements(by=By.XPATH, value="./*")
                if len(icons)==0 or icons[0].get_attribute('data-icon') != 'ban':
                    value_str += v.text + ", "
            value_str = value_str.replace(title,"").replace("\n"," ")
            farm[title] = value_str
        else:
            children = parent.find_elements(by=By.XPATH, value=".//div")
            if (len(children) == 1):
                value_str += children[0].text
            else:
                for c in children:
                    if not 'flex-wrap' in c.get_attribute("class"):
                        value_str += c.text + ", "

        value_str = value_str.replace(title,"").replace("\n"," ")
        farm[title] = value_str


def get_farms_from_page(browser,page_id, url):
    # Load a page
    browser.get(url)
    time.sleep(2)

    wait = WebDriverWait(browser, 10)
    card_body_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card-body")))
    card_body_elements = browser.find_elements(by=By.CSS_SELECTOR, value="div.card-body")
    farms = []
    # Print the text of each card-body element
    for i,card_body_element in enumerate(card_body_elements):
        try:
            card = card_body_element.find_elements(by=By.XPATH, value="./*")[0]
            text_elements = card.find_elements(by=By.XPATH, value="./div|./h6")
            split = text_elements[2].text.split('·')
            f = {
                'page': page_id,
                'card_id': i,
                'place': text_elements[0].text,
                'description': text_elements[1].text,
                'workers': split[0],
                'reviews': split[1],
                'link': 'https://wwoof.fr' + card.get_dom_attribute('href'),
                'error': ''
            }
        except Exception as e:
            f = {
                'page': page_id,
                'card_id': i,
                'error': str(e)
            }
        farms.append(f)
    return farms

def print_file_contents(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            print(line)

def convert_to_csv(data, file_name):
    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Setup a headless browser using Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)

# f= {}
# add_data_from_internal_page(browser, f,'https://wwoof.fr/en/host/34160-association-pedagogique-pour-une-meilleure-connaissance-de-la-foret	')
# print(f)
# exit()


farms = []

total_list_of_columns = set()

for i in range(133,199):
    page_farms = get_farms_from_page(browser,i,"https://wwoof.fr/en/hosts?page=" + str(i))

    for f in page_farms:
        add_data_from_internal_page(browser, f, f['link'])
        for k in f.keys():
            total_list_of_columns.add(k)
        # break

    farms += page_farms
    print(i)
    time.sleep(2)
    file_name = '/Users/hed-bar-nissan/Downloads/tmp.csv'

    #verify the all columns exist on all elements
    for f in farms:
        for c in total_list_of_columns:
            if not c in f: f[c] = ''


    convert_to_csv(farms,file_name)
    # print_file_contents(file_name)

# Clean up
browser.close()
