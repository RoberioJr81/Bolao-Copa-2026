import pandas as pd
import json
import os
import logging
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from tenacity import retry, stop_after_attempt, wait_fixed

# Configuração de Log para você acompanhar o que acontece no Render
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def salvar_json_seguro(nome, dados):
    """Salva os dados atomicamente para nunca corromper o arquivo."""
    temp = nome + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    os.replace(temp, nome)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def conectar():
    # As credenciais vêm do Render (variável de ambiente)
    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(
        creds_dict, 
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    return gspread.authorize(creds).open_by_key(os.environ["SHEET_ID"])

def rodar_motor():
    logging.info("Motor iniciado: Lendo dados da planilha...")
    planilha = conectar()
    
    # Lista de abas que contêm as informações relevantes
    abas = {
        "participantes.json": "C_Participantes",
        "jogos.json": "C_Placares Oficiais",
        "palpites.json": "C_Palpites",
        "ranking_geral.json": "C_Ranking Geral"
    }
    
    for nome_arquivo, nome_aba in abas.items():
        try:
            df = pd.DataFrame(planilha.worksheet(nome_aba).get_all_records())
            # Limpeza: remove valores nulos que quebram o JSON
            df = df.replace({pd.NA: None, float('nan'): None})
            salvar_json_seguro(nome_arquivo, df.to_dict("records"))
            logging.info(f"Arquivo {nome_arquivo} atualizado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao processar {nome_aba}: {e}")

    # Auditoria simples para o app ler
    auditoria = {
        "Status": "OK",
        "Executado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    salvar_json_seguro("auditoria.json", auditoria)
    logging.info("Auditoria gerada.")

if __name__ == "__main__":
    rodar_motor()
