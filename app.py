# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.1
# COMPATÍVEL COM MOTOR OFICIAL v5.5
# ============================================================

import streamlit as st
import pandas as pd
import json
import os


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


PASTA_PUBLICACAO = os.path.join(
    BASE_DIR,
    "publicacao"
)



# ============================================================
# CARREGAR JSON
# ============================================================

def carregar_json(nome):


    caminho = os.path.join(
        PASTA_PUBLICACAO,
        nome
    )


    if not os.path.exists(caminho):

        st.error(
            f"Arquivo não encontrado: {nome}"
        )

        return pd.DataFrame()



    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:


        dados = json.load(
            arquivo
        )


    return pd.DataFrame(
        dados
    )



# ============================================================
# DADOS
# ============================================================

ranking = carregar_json(
    "ranking_geral.json"
)


jogos = carregar_json(
    "jogos.json"
)



# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .titulo{
        font-size:42px;
        font-weight:900;
        color:#006b2e;
        text-align:center;
    }

    .subtitulo{
        text-align:center;
        color:#555;
        margin-bottom:40px;
    }

    .card{
        background:#f8f9fa;
        padding:22px;
        border-radius:18px;
        text-align:center;
        box-shadow:0px 3px 8px #ddd;
    }

    .valor{
        font-size:34px;
        font-weight:bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <div class='titulo'>
    🏆 Bolão Copa do Mundo 2026
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class='subtitulo'>
    Sistema Oficial • Motor v5.5 • FIFA Premium
    </div>
    """,
    unsafe_allow_html=True
)



# ============================================================
# SEGURANÇA
# ============================================================

if ranking.empty:

    st.warning(
        "Ranking aguardando geração pelo motor."
    )


    st.stop()



# ============================================================
# PAINEL
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "👥 Participantes",
        len(ranking)
    )


with c2:

    st.metric(
        "⚽ Jogos",
        len(jogos)
    )


with c3:

    st.metric(
        "🎯 Teto possível",
        "1797 pts"
    )


with c4:


    lider = ranking.sort_values(
        "TOTAL",
        ascending=False
    ).iloc[0]


    st.metric(
        "🏆 Líder",
        lider["Participantes"]
    )



st.divider()



# ============================================================
# ABAS
# ============================================================

aba1, aba2, aba3, aba4 = st.tabs(

    [
        "🏆 Classificação Geral",
        "⚽ Jogos",
        "🥇 Premiações",
        "📜 Critérios"
    ]

)



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with aba1:


    st.subheader(
        "🏆 Ranking Oficial"
    )


    ranking = ranking.sort_values(

        "TOTAL",

        ascending=False

    )


    st.dataframe(

        ranking,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# JOGOS
# ============================================================

with aba2:


    st.subheader(
        "⚽ Jogos Copa 2026"
    )


    st.dataframe(

        jogos,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PREMIAÇÃO
# ============================================================

with aba3:


    st.subheader(
        "🥇 Premiação"
    )


    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(
            "🥇 1º Lugar",
            "Campeão Geral"
        )


    with col2:

        st.metric(
            "🥈 2º Lugar",
            "Vice"
        )


    with col3:

        st.metric(
            "🥉 3º Lugar",
            "Terceiro"
        )



    st.info(
        "Valores finais vinculados à arrecadação oficial do bolão."
    )



# ============================================================
# CRITÉRIOS
# ============================================================

with aba4:


    st.subheader(
        "📜 Critérios de Desempate"
    )


    st.markdown(
        """
        ### Ordem oficial:

        1️⃣ Maior pontuação total

        2️⃣ Maior quantidade de placares exatos

        3️⃣ Maior pontuação nos itens especiais

        4️⃣ Maior antecedência no envio do bolão


        ---
        Critérios aplicados automaticamente pelo motor oficial.
        """
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "🏆 Bolão Copa 2026 — Sistema automático Render + Google Sheets"
)
