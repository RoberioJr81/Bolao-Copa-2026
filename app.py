import streamlit as st
import pandas as pd
import json
import os

from motor import executar_motor


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ============================================================
# EXECUTA MOTOR OFICIAL
# ============================================================

with st.spinner("🔄 Atualizando dados do bolão..."):

    executar_motor()



# ============================================================
# FUNÇÕES
# ============================================================

def carregar_json(nome):


    # primeiro tenta dentro da pasta publicacao

    caminho = os.path.join(
        "publicacao",
        nome
    )


    if not os.path.exists(caminho):

        # compatibilidade com arquivos antigos na raiz

        caminho = nome


    if not os.path.exists(caminho):

        return None


    with open(
        caminho,
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
# CARREGAMENTO DOS DADOS
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

        "titulo":
        "🏆 Bolão Copa do Mundo 2026",

        "participantes":
        len(ranking),

        "jogos":
        len(jogos),

        "teto":
        1797,

        "status":
        "Atualizado automaticamente"

    }



# ============================================================
# CABEÇALHO
# ============================================================

st.title(
    site["titulo"]
)


st.caption(
    "Sistema oficial com atualização automática pelo motor"
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
# ABA INÍCIO
# ============================================================


with aba_inicio:


    st.subheader(

        "🏆 Bolão Copa do Mundo 2026"

    )


    st.write(

        """

        Sistema automático de acompanhamento:

        - atualização pelo Google Sheets;
        - cálculo pelo motor oficial;
        - publicação automática do ranking.

        """

    )


    if not ranking.empty:


        if ranking["TOTAL"].max() == 0:


            st.info(

                "⏳ Copa ainda não iniciada. Ranking definido pelo critério de desempate."

            )


        else:


            lider = ranking.iloc[0]


            st.success(

                f"🏆 Líder atual: {lider['Participante']}"

            )



# ============================================================
# ABA RANKING
# ============================================================


with aba_ranking:


    st.subheader(

        "🏆 Ranking Geral Oficial"

    )


    st.info(

        "Critério de desempate aplicado automaticamente conforme regulamento."

    )


    st.dataframe(

        ranking,

        hide_index=True,

        use_container_width=True

    )



# ============================================================
# ABA PREMIAÇÃO
# ============================================================


with aba_premios:


    st.subheader(

        "🥇 Premiação"

    )


    if premiacao.empty:


        st.info(

            "⏳ Premiação aguardando início da competição."

        )


    else:


        st.dataframe(

            premiacao,

            hide_index=True,

            use_container_width=True

        )



# ============================================================
# ABA JOGOS
# ============================================================


with aba_jogos:


    st.subheader(

        "⚽ Jogos da Copa"

    )


    if jogos.empty:


        st.warning(

            "Jogos ainda não disponíveis."

        )


    else:


        if "Fase" in jogos.columns:


            fase = st.selectbox(

                "Filtrar fase",

                jogos["Fase"].unique()

            )


            jogos = jogos[

                jogos["Fase"] == fase

            ]


        st.dataframe(

            jogos,

            hide_index=True,

            use_container_width=True

        )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(

    "🏆 Bolão Copa 2026 — Motor automático ativo"

)
