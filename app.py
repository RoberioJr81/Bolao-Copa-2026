# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.2
# COMPATÍVEL COM MOTOR OFICIAL v5.5
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
# LOCAL DOS ARQUIVOS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)



# ============================================================
# LEITOR INTELIGENTE DE JSON
# ============================================================

def carregar_json(nome):


    caminhos = [

        os.path.join(
            BASE_DIR,
            nome
        ),

        os.path.join(
            BASE_DIR,
            "publicacao",
            nome
        )

    ]



    for caminho in caminhos:


        if os.path.exists(caminho):


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



    return pd.DataFrame()



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
# AJUSTE DE COMPATIBILIDADE
# ============================================================

if not ranking.empty:


    if "TOTAL" not in ranking.columns:


        if "Total" in ranking.columns:


            ranking = ranking.rename(

                columns={

                    "Total":"TOTAL"

                }

            )



# ============================================================
# CSS FIFA PREMIUM
# ============================================================

st.markdown(
    """
    <style>

    .titulo {

        text-align:center;
        font-size:44px;
        font-weight:900;
        color:#006b2e;

    }


    .subtitulo {

        text-align:center;
        color:#555;
        font-size:18px;

    }


    .topo {

        background:#f8f9fa;
        border-radius:15px;
        padding:20px;
        text-align:center;

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

    <div class="titulo">
    🏆 Bolão Copa do Mundo 2026
    </div>

    """,

    unsafe_allow_html=True

)


st.markdown(

    """

    <div class="subtitulo">
    Sistema Oficial • Motor v5.5 • FIFA Premium
    </div>

    """,

    unsafe_allow_html=True

)



st.divider()



# ============================================================
# VALIDAÇÃO
# ============================================================

if ranking.empty:


    st.error(

        "Classificação ainda não disponível."

    )


    st.stop()



# ============================================================
# PAINEL SUPERIOR
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

        "🎯 Teto máximo",

        "1797 pts"

    )



with c4:


    lider = (

        ranking

        .sort_values(

            "TOTAL",

            ascending=False

        )

        .iloc[0]

    )


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

        "🏆 Classificação",

        "⚽ Jogos",

        "🥇 Premiação",

        "📜 Critérios"

    ]

)



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with aba1:


    st.subheader(

        "🏆 Ranking Geral"

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

        "⚽ Jogos da Copa 2026"

    )


    if jogos.empty:


        st.warning(

            "Jogos não encontrados."

        )


    else:


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

        "🥇 Premiação Oficial"

    )



    col1, col2, col3 = st.columns(3)



    with col1:


        st.metric(

            "🥇 Campeão",

            "1º Geral"

        )



    with col2:


        st.metric(

            "🥈 Vice",

            "2º Geral"

        )



    with col3:


        st.metric(

            "🥉 Terceiro",

            "3º Geral"

        )



    st.info(

        "Premiação vinculada à arrecadação final do bolão."

    )



# ============================================================
# CRITÉRIOS
# ============================================================

with aba4:


    st.subheader(

        "📜 Critérios Oficiais de Desempate"

    )



    st.markdown(

        """

        ### Ordem aplicada:


        **1️⃣ Maior pontuação total**


        **2️⃣ Maior número de placares exatos**


        **3️⃣ Maior pontuação nos critérios especiais**


        **4️⃣ Maior antecedência no envio do bolão**


        ---

        Critérios serão aplicados automaticamente pelo motor oficial.

        """

    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()



st.caption(

    "🏆 Bolão Copa 2026 • Render + Google Sheets • Motor Oficial v5.5"

)
