from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
KEY = 'key.json'
SPREADSHEET_ID = '1wepFNE0w3-3AvFlEqgwDcw9XkZIoBLQGN6m1hzUJd-c'

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def chatbotInsert(tag, msg):
    try:
        values = [[datetime.datetime.now().strftime('%Y-%m-%d, %H:%M'), tag, msg]]
        sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                        range='Chatbot!A1',
                                        valueInputOption='USER_ENTERED',
                                        body={'values':values}).execute()
    except Exception as e:
        print(e)


# Leer
# result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1').execute()
# values = result.get('values',[])
# print(values)

# Escribir
# values = [['Texto insertado']]
# result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='A1', valueInputOption='USER_ENTERED', body={'values':values}).execute()

#chatbotInsert("Prueba","Este es un texto de prueba")