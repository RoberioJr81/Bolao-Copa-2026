import streamlit as st
import pandas as pd
import json


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ============================================================
# FUNÇÕES
# ============================================================

def carregar_json(arquivo):

    with open(
        arquivo,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def carregar_tabela(arquivo):

    return pd.DataFrame(
        carregar_json(arquivo)
    )


# ============================================================
# CARREGAR DADOS
# ============================================================

ranking = carregar_tabela(
    "ranking_geral.json"
)


fase_grupos = carregar_tabela(
    "ranking_fase_grupos.json"
)



# ============================================================
# CABEÇALHO
# ============================================================

st.title(
    "🏆 Bolão Copa do Mundo 2026"
)


st.caption(
    "Sistema oficial de acompanhamento"
)


st.divider()



# ============================================================
# ABAS
# ============================================================

aba_ranking, aba_premios, aba_jogos = st.tabs(

    [

        "🏆 Ranking Geral",

        "🥇 Premiações",

        "⚽ Jogos"

    ]

)



# ============================================================
# ABA RANKING
# ============================================================


with aba_ranking:


    st.subheader(
        "🏆 Classificação Geral"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        use_container_width=True

    )



# ============================================================
# ABA PREMIAÇÕES
# ============================================================


with aba_premios:


    st.subheader(
        "🥇 Premiação — Fase de Grupos"
    )


    top = fase_grupos.head(3)


    colunas = st.columns(
        len(top)
    )


    medalhas = [

        "🥇",

        "🥈",

        "🥉"

    ]


    for i, (_, linha) in enumerate(
        top.iterrows()
    ):


        with colunas[i]:


            st.metric(

                medalhas[i] + " " + str(
                    linha["Participante"]
                ),

                str(
                    linha[
                        "TOTAL PREMIAÇÃO FASE DE GRUPOS"
                    ]
                )
                + " pts"

            )


    st.divider()


    st.write(
        "Classificação completa da premiação:"
    )


    st.dataframe(

        fase_grupos,

        hide_index=True,

        use_container_width=True

    )



# ============================================================
# ABA JOGOS
# ============================================================


with aba_jogos:


    st.subheader(
        "⚽ Jogos da Copa"
    )


    st.info(

        "Tabela de jogos será habilitada na próxima atualização."

    )



# ============================================================
# RODAPÉ
# ============================================================


st.divider()


st.caption(

    "Bolão Copa 2026"

)
