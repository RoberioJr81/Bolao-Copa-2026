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


# ============================================================
# FUNÇÕES
# ============================================================

def carregar_json(nome):

    if not os.path.exists(nome):
        return None

    with open(
        nome,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def carregar_df(nome):

    dados = carregar_json(nome)

    if dados is None:
        return pd.DataFrame()

    return pd.DataFrame(dados)



# ============================================================
# CARREGAMENTO
# ============================================================

ranking = carregar_df(
    "ranking_geral.json"
)


premiacao = carregar_df(
    "premiacao_fase_grupos.json"
)


jogos = carregar_df(
    "jogos.json"
)


site = carregar_json(
    "site.json"
)


if site is None:

    site = {
        "titulo": "🏆 Bolão Copa 2026",
        "participantes": len(ranking),
        "jogos": len(jogos),
        "teto": 1797,
        "status": ""
    }



# ============================================================
# CABEÇALHO
# ============================================================


st.title(
    site["titulo"]
)


st.caption(
    "Sistema oficial de acompanhamento"
)



c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "👥 Participantes",
        site["participantes"]
    )


with c2:

    st.metric(
        "⚽ Jogos",
        site["jogos"]
    )


with c3:

    st.metric(
        "🎯 Teto máximo",
        str(site["teto"]) + " pts"
    )


with c4:

    st.metric(
        "📌 Status",
        site["status"]
    )


st.divider()



# ============================================================
# ABAS
# ============================================================


aba_inicio, aba_ranking, aba_premios, aba_jogos = st.tabs(

    [

        "🏠 Início",

        "🏆 Ranking Oficial",

        "🥇 Premiações",

        "⚽ Jogos"

    ]

)



# ============================================================
# INÍCIO
# ============================================================


with aba_inicio:


    st.subheader(
        "Bem-vindo ao Bolão Copa do Mundo 2026"
    )


    st.write(
        """
        Acompanhe aqui a classificação oficial,
        premiações e evolução dos participantes.
        """
    )


    if not ranking.empty:


        maior = ranking["TOTAL"].max()


        if maior == 0:


            st.info(

                "⏳ Copa ainda não iniciada. Ranking aguardando os primeiros jogos."

            )


        else:


            lider = ranking.iloc[0]


            st.success(

                f"🏆 Líder atual: {lider['Participante']}"

            )



# ============================================================
# RANKING
# ============================================================


with aba_ranking:


    st.subheader(
        "🏆 Ranking Geral Oficial"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        use_container_width=True

    )



# ============================================================
# PREMIAÇÃO
# ============================================================


with aba_premios:


    st.subheader(
        "🥇 Premiação da Fase de Grupos"
    )


    if premiacao.empty:


        st.warning(

            "Premiação não carregada"

        )


    else:


        coluna = (

            "TOTAL PREMIAÇÃO FASE DE GRUPOS"

        )


        if (
            coluna in premiacao.columns
            and premiacao[coluna].max() == 0
        ):


            st.info(

                "⏳ Premiação em disputa. Será definida após a fase de grupos."

            )


        else:


            st.dataframe(

                premiacao,

                hide_index=True,

                use_container_width=True

            )



# ============================================================
# JOGOS
# ============================================================


with aba_jogos:


    st.subheader(
        "⚽ Jogos da Copa"
    )


    if jogos.empty:


        st.warning(

            "Jogos não disponíveis"

        )


    else:


        fases = jogos["Fase"].unique()


        escolha = st.selectbox(

            "Filtrar fase",

            fases

        )


        tabela = jogos[

            jogos["Fase"] == escolha

        ]


        st.dataframe(

            tabela,

            hide_index=True,

            use_container_width=True

        )



# ============================================================
# RODAPÉ
# ============================================================


st.divider()


st.caption(

    "🏆 Bolão Copa do Mundo 2026"

)
