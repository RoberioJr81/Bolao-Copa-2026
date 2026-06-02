import pandas as pd
import json
import os
import logging
import gspread

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def salvar_json_seguro(nome, dados):
    temp = nome + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    os.replace(temp, nome)

def rodar_motor():
    logging.info("Motor iniciado (Modo Público)...")
    try:
        # A nova forma de conectar sem JSON de credenciais
        gc = gspread.service_account_from_dict({}) 
        planilha = gc.open_by_key(os.environ["SHEET_ID"])
        
        abas = {
            "participantes.json": "C_Participantes",
            "jogos.json": "C_Placares Oficiais",
            "palpites.json": "C_Palpites",
            "ranking_geral.json": "C_Ranking Geral"
        }
        
        for nome_arquivo, nome_aba in abas.items():
            aba = planilha.worksheet(nome_aba)
            dados = aba.get_all_records()
            df = pd.DataFrame(dados)
            df = df.replace({pd.NA: None, float('nan'): None})
            salvar_json_seguro(nome_arquivo, df.to_dict("records"))
            logging.info(f"Ficheiro {nome_arquivo} atualizado.")
            
        salvar_json_seguro("auditoria.json", {"Status": "OK", "Executado_em": "Sucesso"})
    except Exception as e:
        logging.error(f"Erro: {e}")
        salvar_json_seguro("auditoria.json", {"Status": "Erro", "Detalhe": str(e)})

if __name__ == "__main__":
    rodar_motor()
