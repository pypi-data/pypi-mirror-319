from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheet:
    def __init__(self,  CREDENCIAL, KEY, PAGINA ):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict = CREDENCIAL, scopes = scope)
        client = authorize(creds)
        sheet = client.open_by_key(KEY)
        self.worksheet = sheet.worksheet(PAGINA)

    def Ler_celulas_listas(self, intervalo = "A1:z"):
        return self.worksheet.get(intervalo)

    def Inserir_listas(self, valor:list[list], intervalo = "A1:z"):
        self.worksheet.update(valor, intervalo)
