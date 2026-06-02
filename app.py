import streamlit as st
import pandas as pd
import json
import os
import subprocess # Adicionado para permitir rodar o motor via botão

st.set_page_config(page_title="🏆 Bolão Copa 2026", layout="wide")

def carregar_json(nome):
    if not os.path.exists(nome): return []
    try:
        with open(nome, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

st.title("🏆 Bolão Copa do Mundo 2026")

# Botão para atualizar (Força o motor a rodar novamente)
if st.sidebar.button("🔄 Atualizar Dados da Planilha"):
    with st.spinner("Sincronizando com o Google Sheets..."):
        subprocess.run(["python", "motor.py"])
        st.success("Dados atualizados!")
        st.rerun()

# Auditoria visual
auditoria = carregar_json("auditoria.json")
if isinstance(auditoria, dict) and auditoria.get("Status") != "OK":
    st.error("Sistema aguardando sincronização.")

aba1, aba2 = st.tabs(["🏆 Ranking Geral", "⚽ Jogos"])

def exibir_tabela(nome_arquivo):
    dados = carregar_json(nome_arquivo)
    if dados:
        df = pd.DataFrame(dados)
        # Oculta o índice para ficar mais limpo
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Dados ainda em processamento.")

with aba1:
    exibir_tabela("ranking_geral.json")

with aba2:
    exibir_tabela("jogos.json")
