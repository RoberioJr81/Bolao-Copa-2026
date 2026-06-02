import pandas as pd
import json
import os
import logging
import gspread
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def salvar_json_seguro(nome, dados):
    temp = nome + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    os.replace(temp, nome)

def rodar_motor():
    logging.info("Motor a iniciar leitura da planilha...")
    try:
        creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        creds = Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        cliente = gspread.authorize(creds)
        planilha = cliente.open_by_key(os.environ["SHEET_ID"])
        
        abas = {
            "participantes.json": "C_Participantes",
            "jogos.json": "C_Placares Oficiais",
            "palpites.json": "C_Palpites",
            "ranking_geral.json": "C_Ranking Geral"
        }
        
        for nome_arquivo, nome_aba in abas.items():
            df = pd.DataFrame(planilha.worksheet(nome_aba).get_all_records())
            df = df.replace({pd.NA: None, float('nan'): None})
            salvar_json_seguro(nome_arquivo, df.to_dict("records"))
            logging.info(f"Ficheiro {nome_arquivo} atualizado.")
            
        auditoria = {"Status": "OK", "Executado_em": "Sucesso"}
        salvar_json_seguro("auditoria.json", auditoria)
        logging.info("Motor concluído com sucesso.")
        
    except Exception as e:
        logging.error(f"Erro no motor: {e}")
        salvar_json_seguro("auditoria.json", {"Status": "Erro", "Detalhe": str(e)})

if __name__ == "__main__":
    rodar_motor()
