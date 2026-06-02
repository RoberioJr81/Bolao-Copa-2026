# ============================================================
# 🏆 APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.7
# COMPATÍVEL COM MOTOR OFICIAL v6.3
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

BASE = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# EXECUTA MOTOR
# ============================================================

try:

    from motor import *

except Exception as erro:

    st.error(
        f"Erro ao executar motor: {erro}"
    )


# ============================================================
# CARREGAR JSON
# ============================================================

def carregar_json(nome):

    caminho = os.path.join(
        BASE,
        nome
    )

    if not os.path.exists(caminho):
        return pd.DataFrame()

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as f:

        dados = json.load(f)


    return pd.DataFrame(
        dados
    )


ranking = carregar_json(
    "ranking_geral.json"
)

jogos = carregar_json(
    "jogos.json"
)

palpites_raw = os.path.join(
    BASE,
    "matriz_palpites.json"
)


# ============================================================
# CARREGAR MATRIZ PALPITES
# ============================================================

def carregar_matriz():

    if not os.path.exists(
        palpites_raw
    ):

        return pd.DataFrame()


    with open(
        palpites_raw,
        "r",
        encoding="utf-8"
    ) as f:

        matriz = json.load(f)


    if len(matriz) < 2:

        return pd.DataFrame()


    cabecalho = matriz[0]

    linhas = matriz[1:]


    return pd.DataFrame(
        linhas,
        columns=cabecalho
    )


palpites = carregar_matriz()


# ============================================================
# CSS PREMIUM
# ============================================================

st.markdown(
"""
<style>

h1,h2,h3 {
    letter-spacing:2px;
}

.titulo {
    text-align:center;
    color:#006b2e;
    font-size:42px;
    font-weight:900;
}

.subtitulo {
    text-align:center;
    color:#555;
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
Sistema Oficial • FIFA Premium • Motor v6.3
</div>
""",
unsafe_allow_html=True
)

st.divider()


# ============================================================
# PROTEÇÃO
# ============================================================

if ranking.empty:

    st.error(
        "Ranking ainda não disponível."
    )

    st.stop()



# ============================================================
# INDICADORES
# ============================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Participantes",
    len(ranking)
)

c2.metric(
    "Jogos",
    len(jogos)
)

c3.metric(
    "Teto máximo",
    "1797 pontos"
)

c4.metric(
    "Líder",
    ranking.iloc[0]["Participantes"]
)


st.divider()



# ============================================================
# ABAS
# ============================================================

aba1,aba2,aba3,aba4,aba5,aba6 = st.tabs(
[
"🏠 Início",
"🏆 Classificação",
"🏅 Premiação",
"⚽ Jogos",
"📋 Palpites",
"📜 Regulamento"
]
)



# ============================================================
# INÍCIO
# ============================================================

with aba1:

    st.header(
        "🏆 Sistema Oficial do Bolão"
    )

    st.success(
        "Motor de classificação automático ativo."
    )

    st.write(
        """
Critérios oficiais de desempate:

1. Acerto do Campeão  
2. Acerto do Artilheiro  
3. Maior pontuação na fase eliminatória  
4. Maior antecedência no envio dos palpites
"""
    )



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with aba2:

    st.header(
        "🏆 Classificação Geral"
    )


    tabela = ranking.copy()


    ocultar = [

        "ID",
        "Data Envio",
        "Enviou"

    ]


    tabela = tabela.drop(

        columns=[

            c for c in ocultar

            if c in tabela.columns

        ],

        errors="ignore"

    )


    renomear = {

        "Fase de Grupo":
        "Item 4.1. Fase de Grupo",

        "Eliminatórias":
        "ITEM 4.3 e 5 - Confrontos Fase Eliminatórias",

        "Campeão":
        "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º",

        "Artilheiro":
        "4.2. Artilheiro",

        "TOTAL":
        "Total"

    }


    tabela = tabela.rename(
        columns=renomear
    )


    st.dataframe(

        tabela,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PREMIAÇÃO
# ============================================================

with aba3:

    st.header(
        "🏅 Premiação Oficial"
    )


    podium = ranking.head(3)


    cols = st.columns(3)


    medalhas = [
        "🥇 1º Lugar",
        "🥈 2º Lugar",
        "🥉 3º Lugar"
    ]


    for i,col in enumerate(cols):

        if i < len(podium):

            with col:

                st.subheader(
                    medalhas[i]
                )

                st.metric(

                    podium.iloc[i]
                    ["Participantes"],

                    str(
                        podium.iloc[i]
                        ["TOTAL"]
                    )
                    +
                    " pontos"

                )


    st.info(
        "Premiação calculada conforme regulamento oficial."
    )



# ============================================================
# JOGOS
# ============================================================

with aba4:

    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    ordem = [

        "Jogo",

        "Data",

        "Local",

        "Seleção A",

        "Placar A",

        "Placar B",

        "Seleção B"

    ]


    mostrar = [

        c for c in ordem

        if c in jogos.columns

    ]


    st.dataframe(

        jogos[mostrar],

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PALPITES
# ============================================================

with aba5:

    st.header(
        "📋 Mapa Geral de Palpites"
    )


    if palpites.empty:

        st.warning(
            "Palpites indisponíveis."
        )

    else:

        st.dataframe(

            palpites,

            hide_index=True,

            width="stretch"

        )



# ============================================================
# REGULAMENTO
# ============================================================

with aba6:

    st.header(
        "📜 Regulamento Oficial"
    )


    st.markdown(
"""
## Item 4.1 - Pontuação dos jogos

🏆 **12 pontos**
- Placar exato

⭐ **8 pontos**
- Resultado correto + gols de uma seleção

✔ **5 pontos**
- Resultado correto

➕ **2 pontos**
- Acerto de gols de uma seleção


---

## Item 4.2 - Premiações Extras

🏆 Campeão da Copa: **25 pontos**

🥈 Vice Campeão: **18 pontos**

🥉 Terceiro Lugar: **12 pontos**

🏅 Quarto Lugar: **10 pontos**

⚽ Artilheiro: **20 pontos**


---

## Passagem de fase

32 avos: **4 pontos**

Oitavas: **8 pontos**

Quartas: **12 pontos**

Semifinal: **16 pontos**

Final: **24 pontos**


---

## Critérios de desempate

1. Campeão  
2. Artilheiro  
3. Fase eliminatória  
4. Ordem de envio

"""
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🏆 Bolão Copa 2026 • FIFA Premium Visual v1.7 • Motor v6.3"
)
