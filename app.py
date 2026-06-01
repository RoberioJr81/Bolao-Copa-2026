

import streamlit as st
import pandas as pd


# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# =====================================================
# CARREGAMENTO DOS DADOS
# =====================================================

ranking = pd.read_csv(
    "ranking_oficial.csv"
).fillna("")


jogos = pd.read_csv(
    "jogos_copa.csv"
).fillna("")


palpites = pd.read_csv(
    "palpites.csv"
).fillna("")


# =====================================================
# ESTILO FIFA PREMIUM
# =====================================================

st.markdown(
"""
<style>

.stApp {
    background: linear-gradient(180deg,#f8fafc,#edf2f7);
}


section[data-testid="stSidebar"] {
    background:#071733;
}


section[data-testid="stSidebar"] * {
    color:white !important;
}


h1 {
    font-size:46px !important;
    font-weight:800 !important;
}


div[data-testid="metric-container"] {

    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 4px 12px rgba(0,0,0,0.08);

}

</style>
""",
unsafe_allow_html=True
)


# =====================================================
# CABEÇALHO FIXO
# =====================================================

st.title(
    "🏆 Bolão Copa do Mundo 2026"
)


st.caption(
    "Painel Oficial FIFA Match Center"
)


st.divider()


# =====================================================
# MENU
# =====================================================

st.sidebar.success(
    "🟢 Sistema Online"
)


pagina = st.sidebar.radio(

    "Navegação",

    [

        "🏅 Classificação",

        "⚽ Jogos",

        "📊 Palpites",

        "💰 Premiação"

    ],

    key="menu_final_fifa_2026"

)



# =====================================================
# CARDS FIXOS
# =====================================================


jogos_finalizados = jogos[

    jogos["status"]
    .astype(str)
    .str.lower()
    .str.contains("encerrado")

].shape[0]


c1,c2,c3 = st.columns(3)


with c1:

    st.metric(

        "Participantes",

        len(ranking)

    )


with c2:

    st.metric(

        "Jogos",

        f"{jogos_finalizados}/104"

    )


with c3:

    st.metric(

        "Fase Real",

        "GRUPOS"

    )


st.divider()



# =====================================================
# FUNÇÃO CLASSIFICAÇÃO
# =====================================================

def tela_classificacao():


    st.subheader(
        "🏅 Ranking Geral"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        use_container_width=True

    )



# =====================================================
# FUNÇÃO JOGOS
# =====================================================


def tela_jogos():


    st.subheader(
        "⚽ Central de Partidas da FIFA"
    )


    tabela = jogos.copy()


    def montar_placar(x):


        if str(x["gols_a"]).strip() == "":

            return "-"


        return (

            str(x["gols_a"])

            +

            " x "

            +

            str(x["gols_b"])

        )



    tabela["Placar"] = tabela.apply(

        montar_placar,

        axis=1

    )


    exibir = pd.DataFrame({

        "📅 Data":

            tabela["data"],


        "🏆 Fase":

            tabela["fase"],


        "Mandante":

            tabela["selecao_a"],


        "Placar":

            tabela["Placar"],


        "Visitante":

            tabela["selecao_b"],


        "📍 Sede":

            tabela["sede"],


        "Status":

            tabela["status"]

    })


    st.dataframe(

        exibir,

        hide_index=True,

        use_container_width=True

    )



# =====================================================
# FUNÇÃO PALPITES
# =====================================================


def tela_palpites():


    st.subheader(
        "📊 Matriz Oficial de Palpites"
    )



    def destaque(row):


        if row["Participante"] == "PLACAR OFICIAL":


            return [

                "background-color:#fff3cd;font-weight:bold"

            ] * len(row)


        return [""] * len(row)



    st.dataframe(

        palpites.style.apply(

            destaque,

            axis=1

        ),

        hide_index=True,

        use_container_width=True

    )



# =====================================================
# FUNÇÃO PREMIAÇÃO
# =====================================================


def tela_premiacao():


    st.subheader(
        "💰 Premiação Oficial do Bolão"
    )


    c1,c2,c3 = st.columns(3)


    with c1:

        st.metric(

            "💵 Valor arrecadado",

            "R$ 6.000,00"

        )


    with c2:

        st.metric(

            "👥 Participantes",

            len(ranking)

        )


    with c3:

        st.metric(

            "💲 Entrada",

            "R$ 200,00"

        )


    vencedores = ranking["Participantes"].head(3)


    st.markdown(
        "## 🏆 Premiação Fase de Grupos"
    )


    st.dataframe(

        pd.DataFrame({

            "Ranking":

            ["🥇 1º","🥈 2º","🥉 3º"],


            "Participante":

            vencedores,


            "Valor":

            [

                "R$ 600,00",

                "R$ 360,00",

                "R$ 240,00"

            ]

        }),

        hide_index=True,

        use_container_width=True

    )



    st.markdown(
        "## 🌍 Premiação Geral do Torneio"
    )


    st.dataframe(

        pd.DataFrame({

            "Ranking":

            ["🥇 1º","🥈 2º","🥉 3º"],


            "Participante":

            vencedores,


            "Valor":

            [

                "R$ 2.880,00",

                "R$ 1.200,00",

                "R$ 720,00"

            ]

        }),

        hide_index=True,

        use_container_width=True

    )



# =====================================================
# CONTROLE FINAL DAS PÁGINAS
# =====================================================


if pagina == "🏅 Classificação":

    tela_classificacao()


elif pagina == "⚽ Jogos":

    tela_jogos()


elif pagina == "📊 Palpites":

    tela_palpites()


elif pagina == "💰 Premiação":

    tela_premiacao()


