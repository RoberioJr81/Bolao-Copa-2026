# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.0
# ============================================================

import streamlit as st
import pandas as pd
import json
import os


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .titulo {
        font-size:42px;
        font-weight:900;
        text-align:center;
        color:#0b6623;
    }

    .subtitulo {
        text-align:center;
        font-size:18px;
        color:#555;
        margin-bottom:30px;
    }

    .card {
        background:#f7f7f7;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0px 2px 8px #ddd;
    }

    .numero {
        font-size:32px;
        font-weight:bold;
        color:#004aad;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# ============================================================
# FUNÇÕES
# ============================================================

PASTA = "publicacao"


def carregar_json(nome):

    caminho = os.path.join(
        PASTA,
        nome
    )


    if not os.path.exists(caminho):

        return pd.DataFrame()


    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)


    return pd.DataFrame(dados)



# ============================================================
# CARREGAMENTO
# ============================================================

ranking = carregar_json(
    "ranking_geral.json"
)


jogos = carregar_json(
    "jogos.json"
)



# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    "<div class='titulo'>🏆 Bolão Copa do Mundo 2026</div>",
    unsafe_allow_html=True
)


st.markdown(
    "<div class='subtitulo'>Sistema Oficial de Ranking • FIFA Premium</div>",
    unsafe_allow_html=True
)



# ============================================================
# VALIDAÇÃO
# ============================================================

if ranking.empty:


    st.error(
        "Ranking ainda não disponível."
    )


    st.stop()



# ============================================================
# PAINEL SUPERIOR
# ============================================================

c1, c2, c3 = st.columns(3)



with c1:

    st.markdown(
        f"""
        <div class='card'>
        Participantes
        <div class='numero'>
        {len(ranking)}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )



with c2:

    st.markdown(
        f"""
        <div class='card'>
        Jogos Copa 2026
        <div class='numero'>
        {len(jogos)}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )



with c3:


    lider = (
        ranking
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .iloc[0]
    )


    st.markdown(
        f"""
        <div class='card'>
        Líder Atual
        <div class='numero'>
        {lider["Participantes"]}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )



st.divider()



# ============================================================
# ABAS
# ============================================================

aba1, aba2, aba3, aba4 = st.tabs(

    [

        "🏅 Ranking",

        "📅 Jogos",

        "💰 Premiação",

        "📜 Critérios"

    ]

)



# ============================================================
# ABA RANKING
# ============================================================

with aba1:


    st.subheader(
        "🏅 Ranking Geral"
    )


    tabela = (

        ranking

        .sort_values(

            "TOTAL",

            ascending=False

        )

    )



    st.dataframe(

        tabela,

        width="stretch",

        hide_index=True

    )



# ============================================================
# ABA JOGOS
# ============================================================

with aba2:


    st.subheader(
        "📅 Jogos da Copa"
    )



    if jogos.empty:


        st.info(

            "Jogos ainda não carregados."

        )


    else:


        st.dataframe(

            jogos,

            width="stretch",

            hide_index=True

        )



# ============================================================
# ABA PREMIAÇÃO
# ============================================================

with aba3:


    st.subheader(
        "💰 Premiação Oficial"
    )



    st.markdown(
        """
        ### 🥇 Campeão
        Maior percentual da premiação


        ### 🥈 Vice-campeão
        Segundo colocado geral


        ### 🥉 Terceiro colocado
        Terceiro colocado geral


        ---

        Os valores serão atualizados conforme arrecadação final do bolão.
        """
    )



# ============================================================
# ABA CRITÉRIOS
# ============================================================

with aba4:


    st.subheader(
        "📜 Critérios de Desempate"
    )



    st.markdown(
        """
        A classificação seguirá os critérios abaixo:


        **1º — Maior pontuação total**

        Soma de todos os itens do regulamento.


        **2º — Maior quantidade de placares exatos**

        Participante com mais acertos completos.


        **3º — Antecedência no envio**

        Persistindo empate, terá vantagem quem enviou primeiro.


        ---


        Sistema automático conectado ao motor oficial do Bolão Copa 2026.
        """
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • Motor v5.5 • FIFA Premium"
)
