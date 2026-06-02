import streamlit as st
import pandas as pd
import json


# ======================================================
# CONFIGURAÇÃO
# ======================================================

st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ======================================================
# EXECUTAR MOTOR
# ======================================================

try:
    from motor import rodar_motor
    rodar_motor()

except Exception as e:

    st.warning(
        "⚠️ Motor não executado. Usando último processamento disponível."
    )

    st.text(str(e))


# ======================================================
# LEITURA SEGURA JSON
# ======================================================

def carregar_lista(nome):

    try:

        with open(nome, "r", encoding="utf-8") as f:

            dados = json.load(f)

            if isinstance(dados, list):
                return dados

            return []

    except:

        return []



def carregar_dict(nome):

    try:

        with open(nome, "r", encoding="utf-8") as f:

            dados = json.load(f)

            if isinstance(dados, dict):
                return dados


            # compatibilidade com JSON antigo
            if isinstance(dados, list):

                if len(dados) > 0:
                    return dados[0]


            return {}

    except:

        return {}



# ======================================================
# CARREGAR DADOS
# ======================================================

ranking = carregar_lista(
    "ranking_geral.json"
)


jogos = carregar_lista(
    "jogos.json"
)


palpites = carregar_lista(
    "palpites.json"
)


participantes = carregar_lista(
    "participantes.json"
)


estatisticas = carregar_dict(
    "estatisticas_bolao.json"
)


premiacao = carregar_dict(
    "premiacao.json"
)


auditoria = carregar_dict(
    "auditoria.json"
)



# ======================================================
# CABEÇALHO
# ======================================================

st.title(
    "🏆 Bolão Copa do Mundo 2026"
)

st.subheader(
    "Sistema oficial • FIFA Premium"
)


c1,c2,c3,c4 = st.columns(4)


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
    "💰 Valor Arrecadado",
    f"R$ {estatisticas.get('Arrecadado',0):,.2f}"
)


c4.metric(
    "🏅 Líder",
    estatisticas.get(
        "Lider",
        "-"
    )
)



st.divider()



# ======================================================
# ABAS
# ======================================================

aba1,aba2,aba3,aba4,aba5,aba6,aba7 = st.tabs(

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
        "Critérios: Pontos → Campeão → Artilheiro → Eliminatórias → Antecedência no envio"
    )


    if ranking:

        st.dataframe(
            pd.DataFrame(ranking),
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


    if jogos:

        st.dataframe(
            pd.DataFrame(jogos),
            width="stretch"
        )

    else:

        st.warning(
            "Nenhum jogo localizado."
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
            pd.DataFrame(palpites),
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


    st.subheader(
        "💰 Valores Arrecadados"
    )


    p1,p2,p3 = st.columns(3)


    p1.metric(
        "Participantes",
        premiacao.get(
            "Participantes",
            estatisticas.get(
                "Participantes",
                0
            )
        )
    )


    p2.metric(
        "Cota",
        f"R$ {premiacao.get('Cota',200):,.2f}"
    )


    p3.metric(
        "Total",
        f"R$ {premiacao.get('Total',0):,.2f}"
    )



    st.divider()



    st.subheader(
        "🏆 Pódio Geral"
    )


    if premiacao.get("Podio Geral"):

        st.table(
            pd.DataFrame(
                premiacao["Podio Geral"]
            )
        )


    st.subheader(
        "🥇 Pódio Fase de Grupo"
    )


    if premiacao.get("Podio Grupo"):

        st.table(
            pd.DataFrame(
                premiacao["Podio Grupo"]
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
        "Todos os inscritos. O participante entra no ranking após envio do palpite."
    )


    if participantes:

        st.dataframe(
            pd.DataFrame(participantes),
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

Resultado correto + gols de uma seleção:
**8 pontos**

Resultado correto:
**5 pontos**

Gols de uma seleção:
**2 pontos**


---

### ITEM 4.2 - Seleções

🏆 Campeão: 25 pontos

🥈 Vice: 18 pontos

🥉 Terceiro: 12 pontos

🏅 Quarto: 10 pontos

⚽ Artilheiro: 20 pontos


### Pontuação de avanço de fase:

32 avos: 4 pontos

Oitavas: 8 pontos

Quartas: 12 pontos

Semifinal: 16 pontos

Final: 24 pontos

"""
)



# ======================================================
# AUDITORIA
# ======================================================

with aba7:


    st.header(
        "🔧 Auditoria do Sistema"
    )


    st.success(
        "Fluxo: Google Sheets → motor.py → JSON → app.py"
    )


    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "Participantes",
        auditoria.get(
            "Participantes",
            "-"
        )
    )


    col2.metric(
        "Efetivados",
        auditoria.get(
            "Efetivados",
            "-"
        )
    )


    col3.metric(
        "Jogos",
        auditoria.get(
            "Jogos",
            "-"
        )
    )


    col4.metric(
        "Ranking",
        auditoria.get(
            "Ranking",
            "-"
        )
    )



st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • FIFA Premium Visual v4.2 • Motor Oficial v8.3"
)
