
from datetime import datetime, timedelta
from google.auth import service_account
from googleapiclient.discovery import build

def duplicate_sheet_per_day(spreadsheet_id, start_date, end_date):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json', scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials)

    date = start_date
    while date <= end_date:
        sheet_title = date.strftime("%Y-%m-%d")
        body = {
            "requests": [
                {
                    "duplicateSheet": {
                        "sourceSheetId": 0,
                        "insertSheetIndex": 1,
                        "newSheetName": sheet_title
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        date += timedelta(days=1)
