import streamlit as st
import pandas as pd
import json
import os

# Configuração da página
st.set_page_config(page_title="🏆 Bolão Copa 2026", page_icon="🏆", layout="wide")

# ======================================================
# FUNÇÃO DE CARREGAMENTO BLINDADO
# ======================================================
def carregar_json(nome, tipo=list):
    """Carrega JSON garantindo que o formato não quebre o app."""
    try:
        if not os.path.exists(nome):
            return {} if tipo == dict else []
        with open(nome, "r", encoding="utf-8") as f:
            dados = json.load(f)
        # Se esperava dict e veio lista, assume o primeiro elemento
        if tipo == dict and isinstance(dados, list):
            return dados[0] if dados else {}
        return dados if isinstance(dados, tipo) else ({} if tipo == dict else [])
    except:
        return {} if tipo == dict else []

# ======================================================
# INTERFACE PRINCIPAL
# ======================================================
st.title("🏆 Bolão Copa do Mundo 2026")
st.caption("Sistema Oficial • FIFA Premium Visual")

# Carregar dados
ranking = carregar_json("ranking_geral.json", list)
jogos = carregar_json("jogos.json", list)
auditoria = carregar_json("auditoria.json", dict)

# Sidebar de Auditoria (Teste de sanidade)
with st.sidebar:
    st.subheader("🔧 Auditoria do Motor")
    st.write(f"**Status:** {auditoria.get('Status', 'Aguardando...')}")
    st.write(f"**Última execução:** {auditoria.get('Executado_em', '-')}")

# Tabs
aba1, aba2 = st.tabs(["🏆 Ranking Geral", "⚽ Jogos"])

with aba1:
    st.header("🏆 Ranking Geral")
    df_ranking = pd.DataFrame(ranking)
    if not df_ranking.empty:
        st.dataframe(df_ranking, use_container_width=True)
    else:
        st.info("Ranking a ser processado pelo motor...")

with aba2:
    st.header("⚽ Tabela de Jogos")
    df_jogos = pd.DataFrame(jogos)
    if not df_jogos.empty:
        st.dataframe(df_jogos, use_container_width=True)
    else:
        st.warning("Tabela de jogos ainda não disponível.")

st.divider()
st.caption("🏆 Bolão 2026 • Motor v9.0 | FIFA Premium Visual v5.0")
