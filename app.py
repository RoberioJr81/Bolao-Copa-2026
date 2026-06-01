

# ============================================================
# APP BOLÃO COPA 2026
# RENDER / STREAMLIT
# ============================================================


import streamlit as st
import pandas as pd
import json
import os


st.set_page_config(

    page_title="Bolão Copa do Mundo 2026",

    layout="wide"

)



st.title("🏆 Bolão Copa do Mundo 2026")



# ============================================================
# FUNÇÃO CARREGAR JSON
# ============================================================


def carregar_json(nome):


    caminho = nome

    )


    with open(

        caminho,

        "r",

        encoding="utf-8"

    ) as arquivo:


        return json.load(

            arquivo

        )



# ============================================================
# CARREGAMENTO
# ============================================================


try:


    ranking = pd.DataFrame(

        carregar_json(

            "ranking_geral.json"

        )

    )


    grupos = pd.DataFrame(

        carregar_json(

            "ranking_fase_grupos.json"

        )

    )


    estatisticas = pd.DataFrame(

        carregar_json(

            "estatisticas_bolao.json"

        )

    )



    # --------------------------------------------------------
    # ESTATÍSTICAS
    # --------------------------------------------------------


    st.subheader("📊 Estatísticas")


    st.dataframe(

        estatisticas,

        use_container_width=True

    )



    # --------------------------------------------------------
    # RANKING GERAL
    # --------------------------------------------------------


    st.subheader("🏆 Ranking Geral")


    st.dataframe(

        ranking,

        use_container_width=True,

        hide_index=True

    )



    # --------------------------------------------------------
    # PREMIAÇÃO GRUPOS
    # --------------------------------------------------------


    st.subheader(

        "🥇 Premiação da Fase de Grupos"

    )


    st.dataframe(

        grupos,

        use_container_width=True,

        hide_index=True

    )



except Exception as erro:


    st.error(

        "Erro ao carregar dados do bolão"

    )


    st.exception(

        erro

    )


