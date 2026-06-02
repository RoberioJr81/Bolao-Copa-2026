# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# FIFA PREMIUM VISUAL v2.0
#
# Compatível com:
# MOTOR OFICIAL v6.5
#
# CORREÇÕES:
# ✅ Ranking usa ordem oficial gerada pelo motor
# ✅ Não recalcula desempate no app
# ✅ Remove aba inicial
# ✅ Corrige Palpites
# ✅ Carrega mapa geral
# ✅ Premiação completa
# ✅ Valores reais do Google Sheets
# ✅ Regulamento completo
# ==============================================================================


import streamlit as st
import pandas as pd
import json
import os


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

        with open(
            nome,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except:

        return padrao



def moeda(valor):

    try:

        return (
            f"R$ {float(valor):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    except:

        return "R$ 0,00"



def tabela(df):

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )


# ==============================================================================
# CARREGAR DADOS
# ==============================================================================


ranking = pd.DataFrame(
    carregar_json(
        "ranking_geral.json",
        []
    )
)


ranking_grupo = pd.DataFrame(
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


stats = carregar_json(
    "estatisticas_bolao.json",
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

    <p style='text-align:center'>
    Sistema Oficial • FIFA Premium • Motor v6.5
    </p>
    """,
    unsafe_allow_html=True
)


c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Participantes",
    stats.get(
        "Participantes",
        len(ranking)
    )
)


c2.metric(
    "Jogos",
    len(jogos)
)


c3.metric(
    "Teto máximo",
    "1797 pontos"
)


lider = "-"

if not ranking.empty:

    lider = ranking.iloc[0]["Participante"]


c4.metric(
    "Líder",
    lider
)


st.divider()



# ==============================================================================
# ABAS
# ==============================================================================


aba1, aba2, aba3, aba4, aba5 = st.tabs(
    [
        "🏆 Classificação",
        "🏅 Premiação",
        "⚽ Jogos",
        "📋 Palpites",
        "📜 Regulamento"
    ]
)



# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================


with aba1:

    st.header(
        "🏆 Classificação"
    )

    if ranking.empty:

        st.warning(
            "Ranking não localizado"
        )

    else:

        tabela(
            ranking
        )



# ==============================================================================
# PREMIAÇÃO
# ==============================================================================


with aba2:


    st.header(
        "🏅 Premiação Oficial"
    )


    st.subheader(
        "💰 Valores arrecadados"
    )


    a,b,c = st.columns(3)


    a.metric(
        "Participantes",
        stats.get(
            "Participantes",
            0
        )
    )


    b.metric(
        "Cota individual",
        moeda(
            stats.get(
                "Cota",
                0
            )
        )
    )


    c.metric(
        "Total arrecadado",
        moeda(
            stats.get(
                "Arrecadado",
                0
            )
        )
    )


    st.divider()


    st.subheader(
        "🏆 Pódio Geral"
    )


    if len(ranking) >= 3:


        premio = [
            0.50,
            0.30,
            0.20
        ]


        cols = st.columns(3)


        for i in range(3):

            jogador = ranking.iloc[i]

            valor = (
                stats.get(
                    "Premiação Geral",
                    0
                )
                *
                premio[i]
            )


            cols[i].metric(

                f"{i+1}º Lugar",

                jogador[
                    "Participante"
                ],

                f'{moeda(valor)} | {jogador["TOTAL"]} pontos'

            )


    st.divider()


    st.subheader(
        "🏆 Pódio - Fase de Grupo"
    )


    if len(ranking_grupo) >= 3:


        cols = st.columns(3)


        for i in range(3):

            jogador = ranking_grupo.iloc[i]


            cols[i].metric(

                f"{i+1}º Lugar",

                jogador[
                    "Participante"
                ],

                f'{jogador["ITEM 4.1. Fase de Grupo"]} pontos'

            )



# ==============================================================================
# JOGOS
# ==============================================================================


with aba3:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    if jogos.empty:

        st.warning(
            "Jogos não localizados"
        )

    else:

        tabela(
            jogos
        )



# ==============================================================================
# PALPITES
# ==============================================================================


with aba4:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if palpites.empty:

        st.warning(
            "Nenhum palpite localizado."
        )

    else:

        tabela(
            palpites
        )



# ==============================================================================
# REGULAMENTO
# ==============================================================================


with aba5:


    st.header(
        "📜 Regulamento"
    )


    st.subheader(
        "ITEM 4.1 - Jogos"
    )


    st.write(
        """
🏆 Placar exato: 12 pontos

⭐ Resultado + gols de uma seleção: 8 pontos

✔ Resultado correto: 5 pontos

➕ Gol de uma seleção: 2 pontos
        """
    )


    st.divider()


    st.subheader(
        "ITEM 4.2 - Seleções e Premiações"
    )


    st.write(
        """

🏆 Campeão: 25 pontos

🥈 Vice-campeão: 18 pontos

🥉 Terceiro lugar: 12 pontos

🏅 Quarto lugar: 10 pontos

⚽ Artilheiro: 20 pontos


Avanço de fase:

• Classificação fase eliminatória

• 16 avos

• Oitavas

• Quartas

• Semifinal

• Final

        """
    )


    st.divider()


    st.subheader(
        "Critérios de desempate"
    )


    st.write(
        """

1. Acerto do Campeão

2. Acerto do Artilheiro

3. Maior pontuação em fases eliminatórias

4. Maior pontuação na fase de grupos

5. Antecedência no envio do palpite

        """
    )



# ==============================================================================
# RODAPÉ
# ==============================================================================


st.divider()

st.caption(
    "🏆 Bolão Copa 2026 • FIFA PREMIUM VISUAL v2.0 • Motor Oficial v6.5"
)
