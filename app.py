# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# APP FIFA PREMIUM v4.0
#
# Apenas apresentação
# Toda lógica está no motor.py
# ==============================================================================


import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ==============================================================================
# EXECUTA MOTOR
# ==============================================================================

try:

    from motor import rodar_motor

    rodar_motor()

    MOTOR_OK = True
    MOTOR_ERRO = ""

except Exception as erro:

    MOTOR_OK = False
    MOTOR_ERRO = str(erro)



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

        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X",".")

    except:

        return "R$ 0,00"



# ==============================================================================
# CARREGAMENTO
# ==============================================================================


ranking = carregar_json(
    "ranking_geral.json",
    []
)


ranking_fase = carregar_json(
    "ranking_fase_grupos.json",
    []
)


participantes = carregar_json(
    "participantes.json",
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


premiacao = carregar_json(
    "premiacao.json",
    {}
)


estatisticas = carregar_json(
    "estatisticas_bolao.json",
    {}
)



# ==============================================================================
# CABEÇALHO
# ==============================================================================


st.title(
    "🏆 Bolão Copa do Mundo 2026"
)


c1, c2, c3, c4 = st.columns(4)



c1.metric(

    "👥 Inscritos",

    estatisticas.get(
        "Participantes",
        0
    )

)


c2.metric(

    "🏆 Participantes Ativos",

    len(ranking)

)


c3.metric(

    "⚽ Jogos",

    estatisticas.get(
        "Jogos",
        "0/0"
    )

)


c4.metric(

    "🥇 Líder",

    estatisticas.get(
        "Lider",
        "-"
    )

)



st.metric(

    "💰 Valor Arrecadado",

    moeda(
        estatisticas.get(
            "Arrecadado",
            0
        )
    )

)



st.divider()



# ==============================================================================
# ABAS
# ==============================================================================


abas = st.tabs(

    [

        "🏆 Classificação",

        "⚽ Jogos",

        "📋 Palpites",

        "🏅 Premiação",

        "👥 Participantes",

        "📜 Regulamento",

        "🔧 Auditoria"

    ]

)



# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================


with abas[0]:


    st.header(
        "🏆 Classificação Geral"
    )


    st.caption(
        "Critérios: Pontos → Campeão → Artilheiro → Eliminatórias → Antecedência no envio"
    )


    if ranking:


        st.dataframe(

            pd.DataFrame(ranking),

            width="stretch",

            hide_index=True

        )


    else:


        st.info(
            "Nenhum palpite enviado ainda."
        )



# ==============================================================================
# JOGOS
# ==============================================================================


with abas[1]:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    st.dataframe(

        pd.DataFrame(jogos),

        width="stretch",

        hide_index=True

    )



# ==============================================================================
# PALPITES
# ==============================================================================


with abas[2]:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    st.dataframe(

        pd.DataFrame(palpites),

        width="stretch",

        hide_index=True

    )



# ==============================================================================
# PREMIAÇÃO
# ==============================================================================


with abas[3]:


    st.header(
        "🏅 Premiação Oficial"
    )


    st.subheader(
        "💰 Valores Arrecadados"
    )


    valores = premiacao.get(
        "Valores Arrecadados",
        {}
    )


    a,b,c = st.columns(3)



    a.metric(

        "Participantes",

        valores.get(
            "Participantes",
            0
        )

    )



    b.metric(

        "Cota",

        moeda(
            valores.get(
                "Cota",
                0
            )
        )

    )



    c.metric(

        "Total",

        moeda(
            valores.get(
                "Total",
                0
            )
        )

    )



    st.subheader(
        "🏆 Pódio Geral"
    )


    st.table(

        pd.DataFrame(

            premiacao.get(
                "Podio Geral",
                []
            )

        )

    )



    st.subheader(
        "🥇 Pódio Fase de Grupo"
    )


    st.table(

        pd.DataFrame(

            premiacao.get(
                "Podio Fase Grupo",
                []
            )

        )

    )



# ==============================================================================
# PARTICIPANTES
# ==============================================================================


with abas[4]:


    st.header(
        "👥 Participantes Inscritos"
    )


    st.caption(

        "Todos os inscritos. O participante entra no ranking após envio do palpite."

    )


    st.dataframe(

        pd.DataFrame(participantes),

        width="stretch",

        hide_index=True

    )



# ==============================================================================
# REGULAMENTO
# ==============================================================================


with abas[5]:


    st.header(
        "📜 Regulamento Oficial"
    )


    st.markdown(
        """

### ITEM 4.1 - Placar dos Jogos

- 🎯 Placar exato: **12 pontos**
- ✅ Resultado + placar de uma seleção: **8 pontos**
- ✔️ Apenas vencedor/empate: **5 pontos**
- ⚽ Um placar correto: **2 pontos**


### ITEM 4.2 - Seleções

- 🏆 Campeão: 25 pontos
- 🥈 Vice-campeão: 18 pontos
- 🥉 Terceiro lugar: 12 pontos
- 🏅 Quarto lugar: 10 pontos
- ⚽ Artilheiro: 20 pontos


### Classificação por fase

- 32 avos: 4 pontos
- Oitavas: 8 pontos
- Quartas: 12 pontos
- Semifinal: 16 pontos
- Final: 24 pontos


### Desempates

1. Maior pontuação total  
2. Campeão  
3. Artilheiro  
4. Fase eliminatória  
5. Antecedência no envio do palpite

"""
    )



# ==============================================================================
# AUDITORIA
# ==============================================================================


with abas[6]:


    st.header(
        "🔧 Auditoria do Sistema"
    )


    st.write(

        "Motor:",

        "✅ OK" if MOTOR_OK else "❌ ERRO"

    )


    if MOTOR_ERRO:

        st.error(
            MOTOR_ERRO
        )


    dados = [

        ["Ranking", len(ranking)],

        ["Participantes", len(participantes)],

        ["Jogos", len(jogos)],

        ["Palpites", len(palpites)],

        ["Premiação", "OK" if premiacao else "Erro"]

    ]


    st.table(

        pd.DataFrame(

            dados,

            columns=[

                "Arquivo",

                "Status"

            ]

        )

    )


    st.caption(

        f"Última atualização: {datetime.now()}"

    )
