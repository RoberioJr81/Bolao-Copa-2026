# ============================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# FIFA PREMIUM VISUAL v1.9
# Compatível Motor Oficial v6.4
# ============================================================

import streamlit as st
import pandas as pd
import json
import os


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    layout="wide"
)


VERSAO = "FIFA PREMIUM VISUAL v1.9 • Motor Oficial v6.4"



# ============================================================
# FUNÇÕES SEGURAS
# ============================================================

def carregar_json(nome):

    if not os.path.exists(nome):
        return []

    try:
        with open(nome, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []



def dataframe_seguro(dados):

    df = pd.DataFrame(dados)

    for c in df.columns:
        df[c] = df[c].astype(str)

    return df



def esconder_colunas(df):

    remover = [
        "_envio",
        "_enviado",
        "_campeao",
        "_artilheiro",
        "ID",
        "Data Envio",
        "Enviou",
        "Peso"
    ]

    return df.drop(
        columns=[
            c for c in remover
            if c in df.columns
        ],
        errors="ignore"
    )



def achar_nome(df):

    for c in df.columns:

        if c.lower() in [
            "participantes",
            "participante",
            "nome"
        ]:
            return c

    return df.columns[0]



# ============================================================
# CARREGAR BASES
# ============================================================

ranking_raw = carregar_json(
    "ranking_geral.json"
)

jogos_raw = carregar_json(
    "jogos.json"
)

matriz_raw = carregar_json(
    "matriz_palpites.json"
)


ranking = dataframe_seguro(
    ranking_raw
)

jogos = dataframe_seguro(
    jogos_raw
)

matriz = dataframe_seguro(
    matriz_raw
)



# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <h1 style='text-align:center;color:#006b2e'>
    🏆 Bolão Copa do Mundo 2026
    </h1>

    <p style='text-align:center'>
    Sistema Oficial • FIFA Premium • Motor v6.4
    </p>

    <hr>
    """,
    unsafe_allow_html=True
)



c1, c2, c3, c4 = st.columns(4)


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


lider = "-"

try:

    nome_col = achar_nome(ranking)

    lider = ranking.iloc[0][nome_col]

except:
    pass


c4.metric(
    "Líder",
    lider
)


st.divider()



# ============================================================
# ABAS
# ============================================================

abas = st.tabs(
    [
        "🏠 Início",
        "🏆 Ranking",
        "🥇 Premiação",
        "⚽ Jogos",
        "📋 Palpites",
        "📜 Regulamento"
    ]
)



# ============================================================
# INÍCIO
# ============================================================

with abas[0]:

    st.header(
        "🏆 Sistema Oficial do Bolão"
    )

    st.success(
        "Motor FIFA Premium ativo."
    )

    st.write(
        "Sistema atualizado com critérios oficiais do regulamento."
    )



# ============================================================
# RANKING
# ============================================================

with abas[1]:

    st.header(
        "🏆 Ranking"
    )


    if ranking.empty:

        st.warning(
            "Ranking ainda não disponível."
        )

    else:

        visual = esconder_colunas(
            ranking
        )

        st.dataframe(
            visual,
            width="stretch",
            hide_index=True
        )



# ============================================================
# PREMIAÇÃO
# ============================================================

with abas[2]:


    st.header(
        "🏅 Premiação Oficial"
    )


    total_participantes = len(ranking)

    arrecadado = (
        total_participantes
        * 100
    )


    st.subheader(
        "💰 Valores"
    )


    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Arrecadação",
        f"R$ {arrecadado:,.2f}"
    )

    c2.metric(
        "Premiação Geral 80%",
        f"R$ {arrecadado*0.8:,.2f}"
    )

    c3.metric(
        "Fase de Grupos 20%",
        f"R$ {arrecadado*0.2:,.2f}"
    )



    st.divider()


    if not ranking.empty:


        podium = esconder_colunas(
            ranking
        ).head(3)


        st.subheader(
            "🏆 Pódio Geral"
        )


        cols = st.columns(3)


        medalhas = [
            "🥇 1º Lugar",
            "🥈 2º Lugar",
            "🥉 3º Lugar"
        ]


        nome_col = achar_nome(
            podium
        )


        for i in range(
            len(podium)
        ):

            cols[i].metric(

                medalhas[i],

                podium.iloc[i][nome_col],

                f"{podium.iloc[i].get('Total','0')} pontos"

            )



        st.divider()


        st.subheader(
            "🏆 Ranking Fase de Grupos"
        )


        if "ITEM 4.1. Fase de Grupo" in ranking.columns:

            fase = ranking.sort_values(
                "ITEM 4.1. Fase de Grupo",
                ascending=False
            )

            fase = esconder_colunas(
                fase
            )

            st.dataframe(
                fase,
                width="stretch",
                hide_index=True
            )



# ============================================================
# JOGOS
# ============================================================

with abas[3]:

    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    if jogos.empty:

        st.warning(
            "Jogos não encontrados."
        )

    else:

        st.dataframe(
            jogos,
            width="stretch",
            hide_index=True
        )



# ============================================================
# PALPITES
# ============================================================

with abas[4]:

    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if matriz.empty:

        st.warning(
            "Nenhum palpite localizado."
        )

    else:

        st.dataframe(
            matriz,
            width="stretch",
            hide_index=True
        )



# ============================================================
# REGULAMENTO
# ============================================================

with abas[5]:


    st.header(
        "📜 Regulamento Oficial"
    )


    st.subheader(
        "ITEM 4.1 - Jogos"
    )


    st.write(
        """
🏆 Placar exato: 12 pontos

⭐ Resultado + gols de uma seleção: 8 pontos

✔ Resultado correto: 5 pontos

➕ Gols de uma seleção: 2 pontos
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


Avanço de fases:

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

3. Maior pontuação nas eliminatórias

4. Maior antecedência no envio dos palpites
        """
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    f"🏆 Bolão Copa 2026 • {VERSAO}"
)
