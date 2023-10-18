import json
from pyhive import presto
import urllib.request


def myLog(str):
    print(str)

API_URL = "http://bo.wix.com/bi-catalog-webapp/api/export/dealer-kpis.json"
TABLE_NAME = "qbox.baguild.dealer_api"

def load_dealer_api(url):
    http_status = -1
    obj = None

    try:

        if (url.startswith('test')):
            text = retrieve_test_JSON_API(url)
        else:
            response = urllib.request.urlopen(url)
            http_status = response.getcode()
            data = response.read()  # a `bytes` object
            text = data.decode('utf-8',errors='ignore')
        obj = json.loads(text)
    except urllib.error.HTTPError as e:
        myLog('[load_dealer_api] HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        myLog('[load_dealer_api] URLError: {}'.format(e.reason))
    except json.decoder.JSONDecodeError:
        myLog("[load_dealer_api] JSON loads error")
    except :
        myLog("[load_dealer_api] error")
        # raise
    return obj


def load_dealer_api_table(table_name):
    obj = None
    try:
        if (table_name.startswith('test')):
            obj = retrieve_test_table(table_name)
        else :
            cursor = presto.connect('presto.wixpress.com', port=8181).cursor()
            sql = 'select date_created, offer_guid, kpi_guids from ' + table_name
            cursor.execute(sql)
            result_set = cursor.fetchall()

    except :
        myLog("[load_dealer_api_table] error")
        # raise
    return obj


def generate_diff_between_dealer_api_and_existing_table():
    current = load_dealer_api(API_URL)
    previous = load_dealer_api_table(TABLE_NAME)






def retrieve_test_JSON_API(test_id):
    json_str = {
        "test1" : '[]'
    } [ test_id ]
    return json_str



def retrieve_test_table(test_id):
    table_as_obj = {
        "test1" : []
    } [ test_id ]
    return table_as_obj


def run_tests():
    ret = load_dealer_api("http://bo.wix.com/bi-catalog-webapp/api/export/404.json")
    assert ret==None
    ret = load_dealer_api("http://bo.wix.com/bi-catalog-webapp")
    assert ret==None
    ret = load_dealer_api("test1")
    assert ret==[]

    ret = load_dealer_api_table("no_table")
    assert ret == None
    ret = load_dealer_api_table("test1")
    assert ret == []

    ret = generate_diff_between_dealer_api_and_existing_table("test1","test1")
    assert ret == []

if __name__ == "__main__":
    run_tests()
