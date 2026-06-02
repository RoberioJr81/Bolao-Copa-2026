# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.3
# MOTOR OFICIAL v5.5
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
# CARREGADOR JSON
# ============================================================

def carregar_json(nome):


    caminhos = [

        os.path.join(
            BASE_DIR,
            nome
        ),

        os.path.join(
            BASE_DIR,
            "publicacao",
            nome
        )

    ]


    for caminho in caminhos:


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



# ============================================================
# DADOS
# ============================================================

ranking = carregar_json(
    "ranking_geral.json"
)


jogos = carregar_json(
    "jogos.json"
)


premiacao = carregar_json(
    "premiacao_fase_grupos.json"
)



# ============================================================
# NORMALIZAÇÃO
# ============================================================

if not ranking.empty:


    # TOTAL

    for coluna in ranking.columns:


        if coluna.lower() == "total":

            ranking = ranking.rename(
                columns={coluna:"TOTAL"}
            )



    # PARTICIPANTE

    for coluna in ranking.columns:


        if "particip" in coluna.lower():

            ranking = ranking.rename(
                columns={coluna:"Participantes"}
            )



# ============================================================
# ESTILO
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
        font-size:18px;
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
    Sistema Oficial • Motor v5.5 • FIFA Premium
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
        "Ranking não encontrado."
    )


    st.stop()



# ============================================================
# TOPO
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Participantes",
        len(ranking)
    )


with col2:

    st.metric(
        "⚽ Jogos",
        len(jogos)
    )


with col3:

    st.metric(
        "🎯 Teto máximo",
        "1797 pontos"
    )


with col4:


    lider = ranking.sort_values(

        "TOTAL",

        ascending=False

    ).iloc[0]


    st.metric(

        "🏆 Líder",

        lider["Participantes"]

    )



st.divider()



# ============================================================
# ABAS
# ============================================================

inicio, classificacao, premios, partidas, estatisticas, regras = st.tabs(

    [

        "🏠 Início",

        "🏆 Classificação",

        "🥇 Premiações",

        "⚽ Jogos",

        "📊 Estatísticas",

        "📜 Regulamento"

    ]

)



# ============================================================
# INÍCIO
# ============================================================

with inicio:


    st.header(
        "🏆 Copa do Mundo 2026"
    )


    st.success(
        "Sistema automático conectado ao Google Sheets e Motor Oficial."
    )


    st.info(
        "Aguardando início da Copa. Ranking será atualizado automaticamente conforme os resultados."
    )



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with classificacao:


    st.header(
        "🏆 Classificação Geral"
    )


    tabela = ranking.sort_values(

        "TOTAL",

        ascending=False

    )


    st.dataframe(

        tabela,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PREMIAÇÕES
# ============================================================

with premios:


    st.header(
        "🥇 Premiações"
    )


    if not premiacao.empty:


        st.dataframe(

            premiacao,

            hide_index=True,

            width="stretch"

        )


    else:


        st.info(

            "Premiações serão exibidas conforme evolução do bolão."

        )



# ============================================================
# JOGOS
# ============================================================

with partidas:


    st.header(
        "⚽ Jogos da Copa"
    )


    st.dataframe(

        jogos,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# ESTATÍSTICAS
# ============================================================

with estatisticas:


    st.header(
        "📊 Estatísticas do Bolão"
    )


    c1,c2,c3 = st.columns(3)



    c1.metric(

        "Participantes",

        len(ranking)

    )


    c2.metric(

        "Jogos cadastrados",

        len(jogos)

    )


    c3.metric(

        "Maior pontuação",

        ranking["TOTAL"].max()

    )



# ============================================================
# REGULAMENTO
# ============================================================

with regras:


    st.header(
        "📜 Regulamento e Critérios"
    )


    st.markdown(
        """

### Pontuação

- Resultado exato da partida;
- Acerto de vencedor ou empate;
- Fase eliminatória;
- Campeão, vice, terceiro e quarto;
- Artilheiro.


---

### Critérios de desempate

1️⃣ Maior pontuação total  

2️⃣ Maior número de placares exatos  

3️⃣ Maior pontuação nos itens especiais  

4️⃣ Maior antecedência no envio do bolão


        """
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • FIFA Premium • Render + Google Sheets"
)
