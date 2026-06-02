import pandas as pd
import json
import os
import gspread

def salvar_json(nome, dados):
    with open(nome, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def rodar_motor():
    try:
        # A magia: Conecta sem precisar de ficheiros extras
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
            salvar_json(nome_arquivo, dados)
            
        salvar_json("auditoria.json", {"Status": "OK"})
    except Exception as e:
        salvar_json("auditoria.json", {"Status": "Erro", "Msg": str(e)})

if __name__ == "__main__":
    rodar_motor()
