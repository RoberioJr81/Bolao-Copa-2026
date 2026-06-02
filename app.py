# ============================================================
# 🏆 APP BOLÃO COPA DO MUNDO 2026
# FIFA PREMIUM VISUAL v1.8
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

BASE = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# EXECUTA MOTOR
# ============================================================

try:
    import motor

except Exception as erro:
    st.error(f"Erro ao executar o motor: {erro}")


# ============================================================
# FUNÇÕES
# ============================================================

def carregar_json(nome):

    caminho = os.path.join(BASE, nome)

    if not os.path.exists(caminho):
        return pd.DataFrame()

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:

        dados = json.load(arquivo)

    return pd.DataFrame(dados)



def localizar_coluna(df, opcoes):

    for coluna in df.columns:

        normal = (
            coluna.lower()
            .replace(" ", "")
            .replace("_", "")
        )

        for opcao in opcoes:

            if normal == opcao:

                return coluna

    return None



def limpar_arrow(df):

    df = df.copy()

    for c in df.columns:

        if df[c].dtype == "object":

            df[c] = df[c].fillna("").astype(str)

    return df



# ============================================================
# CARREGAR BASES
# ============================================================

ranking = carregar_json(
    "ranking_geral.json"
)

jogos = carregar_json(
    "jogos.json"
)

palpites = carregar_json(
    "matriz_palpites.json"
)



# ============================================================
# NORMALIZAÇÃO SEGURA
# ============================================================

COL_NOME = localizar_coluna(
    ranking,
    [
        "participante",
        "participantes",
        "nome",
        "jogador"
    ]
)


COL_TOTAL = localizar_coluna(
    ranking,
    [
        "total",
        "pontos",
        "pontuacao"
    ]
)


if COL_NOME:

    ranking["__NOME__"] = ranking[COL_NOME]

else:

    ranking["__NOME__"] = ""


if COL_TOTAL:

    ranking["__TOTAL__"] = ranking[COL_TOTAL]

else:

    ranking["__TOTAL__"] = 0



# ============================================================
# VISUAL
# ============================================================

st.markdown(
"""
<style>

.titulo {
text-align:center;
font-size:42px;
font-weight:900;
color:#006b2e;
letter-spacing:2px;
}

.sub {
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
<div class="sub">
Sistema Oficial • FIFA Premium • Motor v6.3
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
    ranking.iloc[0]["__NOME__"]
)



st.divider()



# ============================================================
# ABAS
# ============================================================

inicio, geral, premio, aba_jogos, aba_palpites, regulamento = st.tabs(
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

with inicio:

    st.header(
        "🏆 Sistema Oficial do Bolão"
    )


    st.success(
        "Motor de cálculo FIFA Premium ativo."
    )


    st.markdown(
"""
Critérios oficiais de desempate:

1. Acerto do Campeão  
2. Acerto do Artilheiro  
3. Maior pontuação fase eliminatória  
4. Maior antecedência no envio
"""
    )



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with geral:

    st.header(
        "🏆 Classificação Geral"
    )


    tabela = ranking.copy()


    esconder = [

        "ID",
        "Data Envio",
        "Enviou",
        "__NOME__",
        "__TOTAL__",
        "Pesos"

    ]


    tabela.drop(
        columns=[
            c for c in esconder
            if c in tabela.columns
        ],
        inplace=True,
        errors="ignore"
    )


    renomear = {

        COL_NOME:
        "Participantes",

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


    tabela.rename(
        columns=renomear,
        inplace=True
    )


    st.dataframe(
        limpar_arrow(tabela),
        hide_index=True,
        width="stretch"
    )



# ============================================================
# PREMIAÇÃO
# ============================================================

with premio:

    st.header(
        "🏅 Premiação Oficial"
    )


    podium = ranking.head(3)


    colunas = st.columns(3)


    medalhas = [
        "🥇 1º Lugar",
        "🥈 2º Lugar",
        "🥉 3º Lugar"
    ]


    for i, coluna in enumerate(colunas):

        with coluna:

            st.subheader(
                medalhas[i]
            )


            st.metric(
                podium.iloc[i]["__NOME__"],
                str(
                    podium.iloc[i]["__TOTAL__"]
                )
                +
                " pontos"
            )



# ============================================================
# JOGOS
# ============================================================

with aba_jogos:

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


    colunas = [

        c for c in ordem

        if c in jogos.columns

    ]


    st.dataframe(
        limpar_arrow(jogos[colunas]),
        hide_index=True,
        width="stretch"
    )



# ============================================================
# PALPITES
# ============================================================

with aba_palpites:

    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if palpites.empty:

        st.warning(
            "Nenhum palpite localizado."
        )

    else:

        st.dataframe(
            limpar_arrow(palpites),
            hide_index=True,
            width="stretch"
        )



# ============================================================
# REGULAMENTO
# ============================================================

with regulamento:

    st.header(
        "📜 Regulamento Oficial"
    )


    st.markdown(
"""

### ITEM 4.1 - Jogos

🏆 Placar exato: 12 pontos  

⭐ Resultado + gols de uma seleção: 8 pontos  

✔ Resultado correto: 5 pontos  

➕ Gols de uma seleção: 2 pontos  


---

### ITEM 4.2 - Premiações

🏆 Campeão: 25 pontos  

🥈 Vice campeão: 18 pontos  

🥉 Terceiro lugar: 12 pontos  

🏅 Quarto lugar: 10 pontos  

⚽ Artilheiro: 20 pontos  


---

### Critérios de desempate

1. Acerto Campeão  
2. Acerto Artilheiro  
3. Pontos fase eliminatória  
4. Antecedência de envio

"""
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🏆 Bolão Copa 2026 • FIFA PREMIUM VISUAL v1.8 • Motor Oficial v6.3"
)
