import streamlit as st
import pandas as pd
import json
import os


# ======================================================
# CONFIGURAÇÃO
# ======================================================

st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ======================================================
# EXECUTA MOTOR COM SEGURANÇA
# ======================================================

try:
    from motor import rodar_motor

    rodar_motor()

except Exception as erro:

    st.warning(
        "⚠️ Motor não executado. Utilizando último processamento disponível."
    )

    st.caption(str(erro))


# ======================================================
# LEITURA SEGURA
# ======================================================

def carregar_json(nome, tipo):

    try:

        if not os.path.exists(nome):

            return {} if tipo == dict else []


        with open(
            nome,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(arquivo)


        if isinstance(dados, tipo):

            return dados


        return {} if tipo == dict else []


    except Exception:

        return {} if tipo == dict else []



# ======================================================
# CARREGAMENTO
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
# FUNÇÕES VISUAIS
# ======================================================

def tabela_limpa(dados):

    df = pd.DataFrame(dados)

    if df.empty:

        return df


    df = df.dropna(
        axis=1,
        how="all"
    )


    df = df.dropna(
        axis=0,
        how="all"
    )


    return df



def gerar_podio():

    df = pd.DataFrame(ranking)


    if df.empty:

        return pd.DataFrame()


    coluna_pontos = None


    for c in [

        "TOTAL",

        "Total",

        "Pontuação"

    ]:

        if c in df.columns:

            coluna_pontos = c


    if coluna_pontos is None:

        return pd.DataFrame()


    premios = [
        "🥇",
        "🥈",
        "🥉"
    ]


    podio = df.head(3).copy()


    podio.insert(
        0,
        "Medalha",
        premios[:len(podio)]
    )


    return podio[
        [
            "Medalha",
            "Participante",
            coluna_pontos
        ]
    ]



# ======================================================
# CABEÇALHO
# ======================================================


st.title(
    "🏆 Bolão Copa do Mundo 2026"
)


st.caption(
    "Sistema Oficial • FIFA Premium Visual"
)



c1, c2, c3, c4 = st.columns(4)



c1.metric(

    "👥 Participantes",

    estatisticas.get(
        "Participantes",
        0
    )

)



c2.metric(

    "⚽ Jogos",

    f"0/{estatisticas.get('Jogos',0)}"

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
        "🏆 Ranking Geral"
    )


    st.caption(
        "Critérios: Pontuação → Campeão → Artilheiro → Eliminatórias → Antecedência"
    )


    df = pd.DataFrame(ranking)


    if not df.empty:

        st.dataframe(
            df,
            width="stretch"
        )


    else:

        st.info(
            "Ranking aguardando processamento."
        )



# ======================================================
# JOGOS
# ======================================================


with aba2:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    df = tabela_limpa(jogos)


    if not df.empty:

        st.dataframe(
            df,
            width="stretch"
        )


    else:

        st.warning(
            "Jogos não encontrados."
        )



# ======================================================
# PALPITES
# ======================================================


with aba3:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    df = tabela_limpa(palpites)


    if not df.empty:

        st.dataframe(
            df,
            width="stretch"
        )


    else:

        st.info(
            "Nenhum palpite encontrado."
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


    p1, p2, p3 = st.columns(3)


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


    podio = gerar_podio()


    if not podio.empty:

        st.table(podio)


    else:

        st.info(
            "Pódio aguardando ranking."
        )



# ======================================================
# PARTICIPANTES
# ======================================================


with aba5:


    st.header(
        "👥 Participantes Inscritos"
    )


    df = pd.DataFrame(
        participantes
    )


    if not df.empty:

        st.dataframe(
            df,
            width="stretch"
        )



# ======================================================
# REGULAMENTO
# ======================================================


with aba6:


    st.header(
        "📜 Regulamento Oficial"
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


    a1, a2, a3, a4 = st.columns(4)


    a1.metric(
        "Participantes",
        auditoria.get("Participantes",0)
    )


    a2.metric(
        "Efetivados",
        auditoria.get("Efetivados",0)
    )


    a3.metric(
        "Jogos",
        auditoria.get("Jogos",0)
    )


    a4.metric(
        "Ranking",
        auditoria.get("Ranking",0)
    )


    st.json(
        auditoria
    )



# ======================================================
# RODAPÉ
# ======================================================

st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • Motor Oficial v9.0 ESTÁVEL • FIFA Premium Visual v5.0"
)
