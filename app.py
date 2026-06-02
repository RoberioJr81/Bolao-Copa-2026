import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="🏆 Bolão Copa 2026", layout="wide")

def carregar_json(nome):
    if not os.path.exists(nome): return []
    with open(nome, "r", encoding="utf-8") as f:
        return json.load(f)

st.title("🏆 Bolão Copa do Mundo 2026")

# Auditoria visual
auditoria = carregar_json("auditoria.json")
if isinstance(auditoria, dict) and auditoria.get("Status") != "OK":
    st.error("O sistema está a aguardar sincronização com a planilha.")

aba1, aba2 = st.tabs(["🏆 Ranking Geral", "⚽ Jogos"])

with aba1:
    df_ranking = pd.DataFrame(carregar_json("ranking_geral.json"))
    if not df_ranking.empty: st.dataframe(df_ranking, use_container_width=True)
    else: st.info("Dados de ranking em processamento.")

with aba2:
    df_jogos = pd.DataFrame(carregar_json("jogos.json"))
    if not df_jogos.empty: st.dataframe(df_jogos, use_container_width=True)
    else: st.info("Dados de jogos em processamento.")
