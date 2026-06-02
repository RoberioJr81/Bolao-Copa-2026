import streamlit as st
import pandas as pd
import json


# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================

st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ======================================================
# EXECUTA MOTOR
# ======================================================

try:

    from motor import rodar_motor

    rodar_motor()

except Exception as erro:

    st.warning(
        "⚠️ Motor não executado. Utilizando último processamento disponível."
    )

    st.text(str(erro))



# ======================================================
# LEITURA SEGURA JSON
# ======================================================

def carregar_json(nome, tipo):

    try:

        with open(
            nome,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(
                arquivo
            )


        if isinstance(
            dados,
            tipo
        ):

            return dados


        return (
            {}
            if tipo == dict
            else []
        )


    except:

        return (
            {}
            if tipo == dict
            else []
        )



# ======================================================
# CARREGAMENTO DOS JSONs
# ======================================================


ranking = carregar_json(
    "ranking_geral.json",
    list
)


jogos = carregar_json(
    "jogos.json",
    list
)


palpites = carregar_json(
    "palpites.json",
    list
)


participantes = carregar_json(
    "participantes.json",
    list
)


estatisticas = carregar_json(
    "estatisticas_bolao.json",
    dict
)


premiacao = carregar_json(
    "premiacao.json",
    dict
)


auditoria = carregar_json(
    "auditoria.json",
    dict
)



# ======================================================
# CABEÇALHO
# ======================================================


st.title(
    "🏆 Bolão Copa do Mundo 2026"
)


st.caption(
    "Sistema Oficial • FIFA Premium Visual"
)



c1,c2,c3,c4 = st.columns(
    4
)



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
    f"R$ {estatisticas.get('Arrecadado',0):,.2f}"
)



c4.metric(
    "🏆 Líder",
    estatisticas.get(
        "Lider",
        "-"
    )
)


st.divider()



# ======================================================
# ABAS
# ======================================================


aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs(

    [

        "🏆 Ranking",

        "⚽ Jogos",

        "📋 Palpites",

        "🥇 Premiação",

        "👥 Participantes",

        "📜 Regulamento",

        "🔧 Auditoria"

    ]

)



# ======================================================
# RANKING
# ======================================================


with aba1:


    st.header(
        "🏆 Classificação Geral"
    )


    st.caption(
        "Critérios: Pontuação → Campeão → Artilheiro → Eliminatórias → Antecedência"
    )


    if ranking:

        st.dataframe(
            pd.DataFrame(
                ranking
            ),
            width="stretch"
        )

    else:

        st.info(
            "Ranking aguardando dados."
        )



# ======================================================
# JOGOS
# ======================================================


with aba2:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    if jogos:

        st.dataframe(

            pd.DataFrame(
                jogos
            ),

            width="stretch"

        )


    else:

        st.warning(
            "Nenhum jogo encontrado."
        )



# ======================================================
# PALPITES
# ======================================================


with aba3:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if palpites:


        st.dataframe(

            pd.DataFrame(
                palpites
            ),

            width="stretch"

        )


    else:


        st.info(
            "Palpites ainda não carregados."
        )



# ======================================================
# PREMIAÇÃO
# ======================================================


with aba4:


    st.header(
        "🥇 Premiação Oficial"
    )


    valores = premiacao.get(

        "Valores Arrecadados",

        {}

    )


    st.subheader(
        "💰 Valores Arrecadados"
    )


    p1,p2,p3 = st.columns(
        3
    )


    p1.metric(

        "Participantes",

        valores.get(
            "Participantes",
            0
        )

    )


    p2.metric(

        "Cota",

        f"R$ {valores.get('Cota',0):,.2f}"

    )


    p3.metric(

        "Total",

        f"R$ {valores.get('Total',0):,.2f}"

    )


    st.divider()


    st.subheader(
        "🏆 Pódio Geral"
    )


    if premiacao.get(
        "Podio Geral"
    ):


        st.table(

            pd.DataFrame(

                premiacao[
                    "Podio Geral"
                ]

            )

        )



    st.subheader(
        "🥇 Pódio Fase de Grupo"
    )


    if premiacao.get(
        "Podio Grupo"
    ):


        st.table(

            pd.DataFrame(

                premiacao[
                    "Podio Grupo"
                ]

            )

        )



# ======================================================
# PARTICIPANTES
# ======================================================


with aba5:


    st.header(
        "👥 Participantes Inscritos"
    )


    st.caption(
        "Todos os inscritos. O ranking considera apenas participantes efetivados."
    )


    if participantes:


        st.dataframe(

            pd.DataFrame(
                participantes
            ),

            width="stretch"

        )



# ======================================================
# REGULAMENTO
# ======================================================


with aba6:


    st.header(
        "📜 Regulamento"
    )


    st.markdown(
"""

### ITEM 4.1 - Jogos

🏆 Placar exato: **12 pontos**

Resultado correto + gols de uma seleção: **8 pontos**

Resultado correto: **5 pontos**

Gol de uma seleção: **2 pontos**


---

### ITEM 4.2 - Seleções

🏆 Campeão: 25 pontos

🥈 Vice: 18 pontos

🥉 Terceiro: 12 pontos

🏅 Quarto: 10 pontos

⚽ Artilheiro: 20 pontos


### Pontuação de avanço de fase

32 avos: 4 pontos

Oitavas: 8 pontos

Quartas: 12 pontos

Semifinal: 16 pontos

Final: 24 pontos


---

### Desempate

1. Maior pontuação total

2. Campeão

3. Artilheiro

4. Eliminatórias

5. Antecedência no envio

"""
)



# ======================================================
# AUDITORIA
# ======================================================


with aba7:


    st.header(
        "🔧 Auditoria do Sistema"
    )


    a1,a2,a3,a4 = st.columns(
        4
    )


    a1.metric(

        "Participantes",

        auditoria.get(
            "Participantes",
            0
        )

    )


    a2.metric(

        "Efetivados",

        auditoria.get(
            "Efetivados",
            0
        )

    )


    a3.metric(

        "Jogos",

        auditoria.get(
            "Jogos",
            0
        )

    )


    a4.metric(

        "Ranking",

        auditoria.get(
            "Ranking",
            0
        )

    )


    st.json(
        auditoria
    )



st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • Motor Oficial v8.3.2 • FIFA Premium Visual v4.3"
)
