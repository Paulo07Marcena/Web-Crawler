import pandas as pd
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

class dataSend():
    print('Data send init!')

    # Escopos da API Google Sheets e Drive
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    # ID da planilha do Google Sheets (crie uma planilha e pegue o ID da URL)
    SPREADSHEET_ID = '1EucdlGSm5E813bb3I_xGBzJ4Rboj6cDXHKOs-X-Hbto'

    # Nome da aba/guia da planilha onde vai inserir os dados
    SHEET_NAME = 'Vibração-web-crawler'

    # Carregar CSV com pandas
    df = pd.read_csv('files/processed_file.csv')

    # Autenticar com service account
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Criar serviço da API Sheets
    service = build('sheets', 'v4', credentials=creds)

    # Preparar dados para enviar
    values = [df.columns.values.tolist()] + df.values.tolist()

    # Corpo da requisição
    body = {
        'values': values
    }

    # Limpar a aba antes de inserir novos dados (opcional)
    service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()

    # Atualizar valores na planilha
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f"{result.get('updatedCells')} células atualizadas.")

