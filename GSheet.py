from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '.config/service_account.json'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Yx-ki6Vkj9VJ2_BFjjFOPO67AOkKyZ7Lc3LVDGLjOFA'
SAMPLE_RANGE_NAME = 'Working Orders!A2:P'

# Create credentials
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def get_data():

    data = None

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        data = []

        if not values:
            print('No data found.')
            return None
        else:
            for row in values:

                # If name column is empty break out of loop
                if row[1] == '':
                    continue

                # Otherwise iterate through values for what we want to show
                # 1 - Customer
                # 2 - Part Number (Yet to be implemented so this can be not shown for now)
                # 3 - Quantity
                # 4 - Item ordered
                # 5 - Size (Can be lip sizes or length of skirt)
                # 6 - Moulding
                # 10/11 - Shipping/Painting (Boolean one or the other)
                # 12 - Ordered date
                # 13 - Due date
                # 15 - Comments
                # Summary: Don't show columns 2, 7, 8, 9, 14
                print(len(row))

                _row = []
                for x in range(1, 16):
                    if x >= len(row):
                        break
                    if x not in {2, 7, 8, 9, 14}:
                        if row[x] == "TRUE":
                            _row.append(True)
                        elif row[x] == "FALSE":
                            _row.append(False)
                        else:
                            _row.append(row[x])
                data.append(_row)

    except HttpError as err:
        print(err)

    return data


def send_data(new_order):
    try:
        service = build('sheets', 'v4', credentials=creds)

        _values = [
            new_order
        ]
        _body = {
            'values': _values
        }

        # Call the Sheets API
        sheet = service.spreadsheets()

        request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1",
                                                         valueInputOption='USER_ENTERED',
                                                         insertDataOption='INSERT_ROWS', body=_body)
        response = request.execute()
        # print(response)

        # body = {
        #     'values': new_order
        # }
        # result = service.spreadsheets().values().append(
        #     spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()
        # print('{0} cells updated.'.format(result.get('updatedCells')))
    except HttpError as err:
        print(err)
