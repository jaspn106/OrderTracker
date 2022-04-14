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


def get_data():
    # Create credentials
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

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
                # Print columns A and E, which correspond to indices 0 and 4.
                # print('%s, %s' % (row[0], row[4]))
                test_num = 1
                if row[test_num] != '':
                    data.append(row)
                else:
                    break
    except HttpError as err:
        print(err)

    return data
