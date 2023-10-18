
from googleapiclient.discovery import build
import os

sheet_id = '1jL57x_MoMxM580Ty32Kel8qmy5HM6jYFFRRQL_s4Ybw'


def is_cloud_function_env():
    return any(('X_GOOGLE_' in var) for var in os.environ)

def main(request):

    # if request.method == 'OPTIONS':
    #     headers = {
    #         'Access-Control-Allow-Origin': '*',
    #         'Access-Control-Allow-Methods': 'GET',
    #         'Access-Control-Allow-Headers': 'Content-Type',
    #         'Access-Control-Max-Age': '3600'
    #     }
    #     return ('', 204, headers)


    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    service = build('sheets', 'v4')
    sheet = service.spreadsheets()

    i = 1
    ret = ''

    grandchildren = {}
    while True:
        sheet_range = 'Sheet1!A{}:C{}'.format(i,i)
        i += 1

        if i == 2:
            continue

        tmp_line = sheet.values().get(spreadsheetId=sheet_id,
                                        range=sheet_range).execute()
        if 'values' not in tmp_line: break
        tmp_line = tmp_line['values'][0]

        if tmp_line[0] not in grandchildren:
            grandchildren[tmp_line[0]] = {'name': tmp_line[0], 'imgs':[], 'sounds':[] }
        grandchild = grandchildren[tmp_line[0]]
        if tmp_line[1] == "Image":
            grandchild['imgs'].append(tmp_line[2])
        elif tmp_line[1] == "Sound":
            grandchild['sounds'].append(tmp_line[2])

    grandchildren_arr = []
    for g in grandchildren.values():
        grandchildren_arr.append(g)

    ret = str(grandchildren_arr)
    ret = ret.replace("'",'"')
    return (ret, 200, headers)


if __name__ == "__main__":
    if not is_cloud_function_env():
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ["HOME"] + '/.keys/kiss-a-grandchild-865bbc6f6313.json'


    ret = main(None)
    print(ret)