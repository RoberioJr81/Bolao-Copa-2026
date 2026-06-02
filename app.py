# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# FIFA PREMIUM VISUAL v3.2
#
# Compatível:
# MOTOR OFICIAL v8.1
#
# APP NÃO CALCULA REGRA DO BOLÃO
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
            .replace("X",".")
        )

    except:

        return "R$ 0,00"



def tabela(dados):

    df = pd.DataFrame(dados)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )


# ==============================================================================
# CARREGAMENTO JSON
# ==============================================================================


ranking = carregar_json(
    "ranking_geral.json",
    []
)


ranking_grupos = carregar_json(
    "ranking_fase_grupos.json",
    []
)


jogos = carregar_json(
    "jogos.json",
    []
)


palpites = carregar_json(
    "palpites.json",
    []
)


participantes = carregar_json(
    "participantes.json",
    []
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



lider = "-"

if ranking:

    lider = ranking[0].get(
        "Participante",
        "-"
    )



c1,c2,c3,c4 = st.columns(4)



c1.metric(

    "👥 Participantes",

    estatisticas.get(
        "Participantes",
        0
    )

)



c2.metric(

    "⚽ Jogos",

    estatisticas.get(
        "Jogos",
        "0/104"
    )

)



c3.metric(

    "💰 Arrecadado",

    moeda(
        estatisticas.get(
            "Arrecadado",
            0
        )
    )

)



c4.metric(

    "🥇 Líder",

    lider

)



st.divider()



# ==============================================================================
# ABAS
# ==============================================================================


aba1,aba2,aba3,aba4,aba5,aba6 = st.tabs(

[

"🏆 Classificação",

"⚽ Jogos",

"📋 Palpites",

"🏅 Premiação",

"👥 Participantes",

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


    if ranking:

        tabela(
            ranking
        )


    else:


        st.warning(
            "Ranking não disponível."
        )



# ==============================================================================
# JOGOS
# ==============================================================================


with aba2:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    if jogos:


        tabela(
            jogos
        )


    else:


        st.warning(
            "Nenhum jogo encontrado."
        )



# ==============================================================================
# PALPITES
# ==============================================================================


with aba3:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if palpites:


        tabela(
            palpites
        )


    else:


        st.warning(
            "Nenhum palpite encontrado."
        )



# ==============================================================================
# PREMIAÇÃO
# ==============================================================================


with aba4:


    st.header(
        "🏅 Premiação Oficial"
    )


    st.subheader(
        "💰 Valores Arrecadados"
    )



    a,b,c = st.columns(3)



    a.metric(

        "Participantes",

        estatisticas.get(
            "Participantes",
            0
        )

    )



    b.metric(

        "Cota Individual",

        moeda(
            estatisticas.get(
                "Cota",
                0
            )
        )

    )



    c.metric(

        "Total",

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
            min(
                3,
                len(podio)
            )
        )


        for i,j in enumerate(
            podio[:3]
        ):


            cols[i].metric(

                f"{i+1}º Lugar",

                j.get(
                    "Participante",
                    "-"
                ),

                f'{j.get("TOTAL",0)} pontos'

            )



    st.subheader(
        "🏆 Pódio Fase de Grupo"
    )


    grupo = premiacao.get(
        "Podio Fase Grupo",
        []
    )


    if grupo:


        cols = st.columns(
            min(
                3,
                len(grupo)
            )
        )


        for i,j in enumerate(
            grupo[:3]
        ):


            cols[i].metric(

                f"{i+1}º Lugar",

                j.get(
                    "Participante",
                    "-"
                ),

                f'{j.get("ITEM 4.1. Fase de Grupo",0)} pontos'

            )



# ==============================================================================
# PARTICIPANTES
# ==============================================================================


with aba5:


    st.header(
        "👥 Participantes Inscritos"
    )


    if participantes:


        tabela(
            participantes
        )


    else:


        st.warning(
            "Participantes não encontrados."
        )



# ==============================================================================
# REGULAMENTO
# ==============================================================================


with aba6:


    st.header(
        "📜 Regulamento Oficial"
    )



    st.subheader(
        "Item 4.1 - Placares"
    )


    st.write(
"""
🏆 Placar exato: **12 pontos**

⭐ Resultado + gols de uma seleção: **8 pontos**

✔ Resultado correto: **5 pontos**

➕ Gol de uma seleção: **2 pontos**
"""
)



    st.subheader(
        "Item 4.2 - Seleções"
    )


    st.write(
"""
🏆 Campeão: **25 pontos**

🥈 Vice-campeão: **18 pontos**

🥉 Terceiro lugar: **12 pontos**

🏅 Quarto lugar: **10 pontos**

⚽ Artilheiro: **20 pontos**


Classificações:

• 32 avos: 4 pontos

• Oitavas: 8 pontos

• Quartas: 12 pontos

• Semifinal: 16 pontos

• Final: 24 pontos
"""
)



    st.subheader(
        "Critérios de desempate"
    )


    st.write(
"""
1️⃣ Acerto do Campeão

2️⃣ Acerto do Artilheiro

3️⃣ Maior pontuação na fase eliminatória

4️⃣ Antecedência no envio do palpite
"""
)



# ==============================================================================
# RODAPÉ
# ==============================================================================


st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • FIFA PREMIUM VISUAL v3.2 • Motor Oficial v8.1"
)
