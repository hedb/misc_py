import requests
from bs4 import BeautifulSoup
import json



def fetch_companies_json(session,segment_id,cookies):
    data = {
        "collectionName": "EcosystemMap-Startups",
        "dataQuery": {
            "filter": {
                "mainChallenge": {
                    "$hasSome": [
                        "AAAAA"
                    ]
                }
            },
            "paging": {
                "offset": 0,
                "limit": 50
            }
        },
        "options": {},
        "includeReferencedItems": [],
        "segment": "LIVE",
        "appId": "b0c649d8-3091-4766-950c-979f32bb06bd"
    }

    data = json.dumps(data).replace( 'AAAAA', segment_id)

    print(cookies)
    response = session.post('https://www.planetech.org/_api/cloud-data/v1/wix-data/collections/query', json=data, cookies=cookies)

    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
    else:
        print('Error:', response.status_code)


def main():

    main_page_URL = "https://www.planetech.org/startups-platform"

    session = requests.Session()
    response = session.get(main_page_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.find_all("div", {"data-testid": "linkElement"})

    for div in divs:
        # print(div)
        image = div.find('wix-image');
        if image != None and 'data-image-info' in image.attrs:
            image_id = image.attrs['id']
            query_id = image_id.split("__", 1)[1]
            image_info_string = image.attrs['data-image-info']
            image_info = json.loads(image_info_string)
            image_name = image_info['imageData']['name']
            image_name = image_name.replace('.png', '')
            print(image_name, query_id)
            fetch_companies_json(session,query_id,response.cookies)
            exit(1)


if __name__ == "__main__":
    main()