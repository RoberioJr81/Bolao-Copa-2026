# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.5
# COMPATÍVEL COM MOTOR OFICIAL v6.1
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


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)



# ============================================================
# ATUALIZAÇÃO AUTOMÁTICA PELO MOTOR
# ============================================================

try:

    from motor import executar_motor


    with st.spinner(
        "Atualizando informações oficiais..."
    ):

        executar_motor()


except Exception as erro:

    st.warning(
        f"Motor não executado: {erro}"
    )



# ============================================================
# LEITURA JSON
# ============================================================

def carregar_json(nome):

    caminho = os.path.join(
        BASE_DIR,
        nome
    )


    if os.path.exists(caminho):

        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as arquivo:


            return pd.DataFrame(
                json.load(arquivo)
            )


    return pd.DataFrame()



ranking = carregar_json(
    "ranking_geral.json"
)


jogos = carregar_json(
    "jogos.json"
)


matriz = carregar_json(
    "matriz_palpites.json"
)



# ============================================================
# CSS
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
    Sistema Oficial • FIFA Premium • Motor v6.1
    </div>
    """,

    unsafe_allow_html=True
)


st.divider()



# ============================================================
# SEGURANÇA
# ============================================================

if ranking.empty:


    st.error(
        "Ranking não disponível."
    )


    st.stop()



# ============================================================
# PAINEL
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
    "1797 pts"
)


c4.metric(
    "Líder",
    ranking.iloc[0]["Participantes"]
)



st.divider()



# ============================================================
# ABAS
# ============================================================

inicio, classificacao, premiacao, jogos_tab, palpites_tab, regulamento = st.tabs(

    [

        "Início",

        "Classificação Geral",

        "Premiação",

        "Jogos",

        "Palpites",

        "Regulamento"

    ]

)



# ============================================================
# INÍCIO
# ============================================================

with inicio:


    st.header(
        "Painel Oficial"
    )


    st.success(
        "Dados sincronizados automaticamente com Google Sheets."
    )


    st.write(
        "Sistema oficial do Bolão Copa do Mundo 2026."
    )



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with classificacao:


    st.header(
        "Classificação Geral"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PREMIAÇÃO COM PÓDIO
# ============================================================

with premiacao:


    st.header(
        "Premiação Oficial"
    )


    top3 = ranking.head(3)


    col1,col2,col3 = st.columns(3)



    if len(top3) >= 1:

        with col1:

            st.subheader("🥇 1º Lugar")

            st.metric(
                top3.iloc[0]["Participantes"],
                str(top3.iloc[0]["TOTAL"])+" pts"
            )



    if len(top3) >= 2:

        with col2:

            st.subheader("🥈 2º Lugar")

            st.metric(
                top3.iloc[1]["Participantes"],
                str(top3.iloc[1]["TOTAL"])+" pts"
            )



    if len(top3) >= 3:

        with col3:

            st.subheader("🥉 3º Lugar")

            st.metric(
                top3.iloc[2]["Participantes"],
                str(top3.iloc[2]["TOTAL"])+" pts"
            )



    st.info(
        "Premiação calculada conforme regulamento oficial."
    )



# ============================================================
# JOGOS
# ============================================================

with jogos_tab:


    st.header(
        "Tabela Completa de Jogos"
    )


    st.dataframe(

        jogos,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PALPITES - MATRIZ OFICIAL
# ============================================================

with palpites_tab:


    st.header(
        "Mapa Geral de Palpites"
    )


    if matriz.empty:


        st.warning(
            "Matriz de palpites ainda não disponível."
        )


    else:


        st.dataframe(

            matriz,

            hide_index=True,

            width="stretch"

        )



# ============================================================
# REGULAMENTO
# ============================================================

with regulamento:


    st.header(
        "Regulamento Oficial"
    )


    st.markdown(
        """

### Pontuação - Fase de Grupos

**12 pontos**  
Placar exato


**8 pontos**  
Vencedor + placar de uma seleção


**5 pontos**  
Vencedor ou empate correto


**2 pontos**  
Um placar correto


---

### Critérios de Desempate

1. Acerto do Campeão

2. Acerto do Artilheiro

3. Maior pontuação na fase eliminatória

4. Maior antecedência no envio da planilha oficial

        """
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "Bolão Copa 2026 • Render + Google Sheets • Motor v6.1"
)
