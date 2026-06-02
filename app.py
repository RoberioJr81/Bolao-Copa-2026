# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# FIFA PREMIUM VISUAL v3.0
#
# Compatível:
# MOTOR OFICIAL v7.1
#
# O APP NÃO CALCULA NADA
# Apenas apresenta os JSONs oficiais
# ==============================================================================


import streamlit as st
import pandas as pd
import json


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================


st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ==============================================================================
# FUNÇÕES
# ==============================================================================


def carregar_json(nome, padrao):

    try:

        with open(nome, "r", encoding="utf-8") as arquivo:

            return json.load(arquivo)

    except:

        return padrao



def moeda(valor):

    try:

        return (
            f"R$ {float(valor):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X",".")
        )

    except:

        return "R$ 0,00"



def tabela(df):

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )


# ==============================================================================
# CARREGAMENTO DOS JSONS
# ==============================================================================


ranking = pd.DataFrame(
    carregar_json(
        "ranking_geral.json",
        []
    )
)


ranking_grupos = pd.DataFrame(
    carregar_json(
        "ranking_fase_grupos.json",
        []
    )
)


jogos = pd.DataFrame(
    carregar_json(
        "jogos.json",
        []
    )
)


palpites = pd.DataFrame(
    carregar_json(
        "palpites.json",
        []
    )
)


estatisticas = carregar_json(
    "estatisticas_bolao.json",
    {}
)


premiacao = carregar_json(
    "premiacao.json",
    {}
)


# ==============================================================================
# CABEÇALHO
# ==============================================================================


st.markdown(
"""
<h1 style='text-align:center;color:#006b2e'>
🏆 Bolão Copa do Mundo 2026
</h1>

<h4 style='text-align:center'>
Sistema Oficial • FIFA Premium
</h4>

""",
unsafe_allow_html=True
)


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "👥 Participantes",
    estatisticas.get(
        "Participantes",
        "-"
    )
)


c2.metric(
    "⚽ Jogos",
    len(jogos)
)


c3.metric(
    "🏆 Teto máximo",
    "1797 pontos"
)


lider = "-"


if not ranking.empty:

    lider = ranking.iloc[0][
        "Participante"
    ]


c4.metric(
    "🥇 Líder",
    lider
)


st.divider()


# ==============================================================================
# ABAS
# ==============================================================================


aba1,aba2,aba3,aba4,aba5 = st.tabs(

[

"🏆 Classificação",

"⚽ Jogos",

"📋 Palpites",

"🏅 Premiação",

"📜 Regulamento"

]

)


# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================


with aba1:


    st.header(
        "🏆 Classificação Geral"
    )


    if ranking.empty:

        st.warning(
            "Ranking ainda não disponível"
        )

    else:

        tabela(
            ranking
        )


# ==============================================================================
# JOGOS
# ==============================================================================


with aba2:


    st.header(
        "⚽ Jogos Oficiais"
    )


    if jogos.empty:


        st.warning(
            "Nenhum jogo encontrado"
        )


    else:


        tabela(
            jogos
        )


# ==============================================================================
# PALPITES
# ==============================================================================


with aba3:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if palpites.empty:


        st.warning(
            "Palpites não encontrados"
        )


    else:


        tabela(
            palpites
        )


# ==============================================================================
# PREMIAÇÃO
# ==============================================================================


with aba4:


    st.header(
        "🏅 Premiação Oficial"
    )


    st.subheader(
        "💰 Valores arrecadados"
    )


    a,b,c = st.columns(3)


    a.metric(

        "Participantes",

        estatisticas.get(
            "Participantes",
            "-"
        )

    )


    b.metric(

        "Cota individual",

        moeda(
            estatisticas.get(
                "Cota",
                0
            )
        )

    )


    c.metric(

        "Total arrecadado",

        moeda(
            estatisticas.get(
                "Arrecadado",
                0
            )
        )

    )


    st.divider()


    st.subheader(
        "🏆 Pódio Geral"
    )


    podio = premiacao.get(
        "Podio Geral",
        []
    )


    if podio:


        cols = st.columns(
            len(podio)
        )


        for i,jogador in enumerate(podio):


            cols[i].metric(

                f"{i+1}º Lugar",

                jogador.get(
                    "Participante",
                    "-"
                ),

                f'{jogador.get("TOTAL",0)} pontos'

            )


    st.divider()



    st.subheader(
        "🏆 Pódio Fase de Grupo"
    )


    if not ranking_grupos.empty:


        cols = st.columns(3)


        for i in range(
            min(
                3,
                len(ranking_grupos)
            )
        ):


            jogador = ranking_grupos.iloc[i]


            cols[i].metric(

                f"{i+1}º Lugar",

                jogador[
                    "Participante"
                ],

                f'{jogador["ITEM 4.1. Fase de Grupo"]} pontos'

            )


# ==============================================================================
# REGULAMENTO
# ==============================================================================


with aba5:


    st.header(
        "📜 Regulamento Oficial"
    )


    st.subheader(
        "Item 4.1 - Placares"
    )


    st.write(
"""
🏆 Placar exato: 12 pontos

⭐ Resultado + gol de uma seleção: 8 pontos

✔ Resultado correto: 5 pontos

➕ Gol de uma seleção: 2 pontos
"""
)


    st.subheader(
        "Critérios de desempate"
    )


    st.write(
"""
1️⃣ Acerto do Campeão

2️⃣ Acerto do Artilheiro

3️⃣ Maior pontuação fase eliminatória

4️⃣ Antecedência no envio do palpite
"""
)


# ==============================================================================
# RODAPÉ
# ==============================================================================


st.divider()


st.caption(
"🏆 Bolão Copa 2026 • FIFA PREMIUM VISUAL v3.0 • Motor Oficial v7.1"
)
