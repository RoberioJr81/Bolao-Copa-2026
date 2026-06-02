# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# FIFA PREMIUM VISUAL v3.2.1
#
# Compatível com:
# MOTOR OFICIAL v8.1
#
# O APP NÃO CALCULA RESULTADOS
# Apenas apresenta JSONs gerados pelo motor
# ==============================================================================


import streamlit as st
import pandas as pd
import json


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="🏆 Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ==============================================================================
# FUNÇÕES
# ==============================================================================

def carregar_json(nome, padrao):

    try:

        with open(
            nome,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(arquivo)


        # garante tipo correto

        if isinstance(padrao, dict):

            if isinstance(dados, dict):
                return dados

            return padrao


        if isinstance(padrao, list):

            if isinstance(dados, list):
                return dados

            return padrao


        return dados


    except Exception as erro:

        print(
            f"Falha carregando {nome}: {erro}"
        )

        return padrao



def moeda(valor):

    try:

        return (
            f"R$ {float(valor):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    except:

        return "R$ 0,00"



def mostrar_tabela(dados):

    df = pd.DataFrame(dados)

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )


# ==============================================================================
# CARREGAMENTO DOS JSONS OFICIAIS
# ==============================================================================


ranking = carregar_json(
    "ranking_geral.json",
    []
)


ranking_grupos = carregar_json(
    "ranking_fase_grupos.json",
    []
)


jogos = carregar_json(
    "jogos.json",
    []
)


palpites = carregar_json(
    "palpites.json",
    []
)


participantes = carregar_json(
    "participantes.json",
    []
)


estatisticas = carregar_json(
    "estatisticas_bolao.json",
    {}
)


premiacao = carregar_json(
    "premiacao.json",
    {}
)



# ==============================================================================
# CABEÇALHO
# ==============================================================================


st.markdown(
"""
<h1 style='text-align:center;color:#006b2e'>
🏆 Bolão Copa do Mundo 2026
</h1>

<h4 style='text-align:center'>
Sistema Oficial • FIFA Premium
</h4>
""",
unsafe_allow_html=True
)



lider = "-"


if ranking:

    lider = ranking[0].get(
        "Participante",
        "-"
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
    "💰 Arrecadado",
    moeda(
        estatisticas.get(
            "Arrecadado",
            0
        )
    )
)



c4.metric(
    "🥇 Líder",
    lider
)



st.divider()



# ==============================================================================
# ABAS
# ==============================================================================


aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(
    [
        "🏆 Classificação",
        "⚽ Jogos",
        "📋 Palpites",
        "🏅 Premiação",
        "👥 Participantes",
        "📜 Regulamento"
    ]
)



# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================


with aba1:

    st.header(
        "🏆 Classificação Geral"
    )


    if ranking:

        mostrar_tabela(
            ranking
        )

    else:

        st.info(
            "Ranking aguardando processamento."
        )



# ==============================================================================
# JOGOS
# ==============================================================================


with aba2:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    if jogos:

        mostrar_tabela(
            jogos
        )

    else:

        st.info(
            "Nenhum jogo encontrado."
        )



# ==============================================================================
# PALPITES
# ==============================================================================


with aba3:


    st.header(
        "📋 Mapa Geral dos Palpites"
    )


    if palpites:

        mostrar_tabela(
            palpites
        )

    else:

        st.info(
            "Nenhum palpite encontrado."
        )



# ==============================================================================
# PREMIAÇÃO
# ==============================================================================


with aba4:


    st.header(
        "🏅 Premiação Oficial"
    )


    st.subheader(
        "💰 Valores Arrecadados"
    )


    a,b,c = st.columns(3)


    a.metric(
        "Participantes",
        estatisticas.get(
            "Participantes",
            0
        )
    )


    b.metric(
        "Cota Individual",
        moeda(
            estatisticas.get(
                "Cota",
                0
            )
        )
    )


    c.metric(
        "Total",
        moeda(
            estatisticas.get(
                "Arrecadado",
                0
            )
        )
    )


    st.divider()


    st.subheader(
        "🏆 Pódio Geral"
    )


    podio = premiacao.get(
        "Podio Geral",
        []
    )


    if podio:

        mostrar_tabela(
            podio
        )



    st.subheader(
        "🏆 Pódio Fase de Grupo"
    )


    podio_grupo = premiacao.get(
        "Podio Fase Grupo",
        []
    )


    if podio_grupo:

        mostrar_tabela(
            podio_grupo
        )



# ==============================================================================
# PARTICIPANTES
# ==============================================================================


with aba5:


    st.header(
        "👥 Participantes Inscritos"
    )


    if participantes:

        mostrar_tabela(
            participantes
        )



# ==============================================================================
# REGULAMENTO
# ==============================================================================


with aba6:


    st.header(
        "📜 Regulamento Oficial"
    )


    st.subheader(
        "ITEM 4.1 - Jogos"
    )


    st.markdown(
"""
🏆 **Placar exato:** 12 pontos

⭐ **Resultado + gols de uma seleção:** 8 pontos

✔️ **Resultado correto:** 5 pontos

➕ **Gol de uma seleção:** 2 pontos
"""
    )


    st.subheader(
        "ITEM 4.2 - Seleções"
    )


    st.markdown(
"""
🏆 Campeão: **25 pontos**

🥈 Vice: **18 pontos**

🥉 Terceiro: **12 pontos**

🏅 Quarto: **10 pontos**

⚽ Artilheiro: **20 pontos**

Classificações:

- 32 avos: 4 pontos
- Oitavas: 8 pontos
- Quartas: 12 pontos
- Semifinal: 16 pontos
- Final: 24 pontos
"""
    )


    st.subheader(
        "Critérios de desempate"
    )


    st.markdown(
"""
1️⃣ Acerto do Campeão

2️⃣ Acerto do Artilheiro

3️⃣ Maior pontuação na fase eliminatória

4️⃣ Antecedência no envio do palpite
"""
    )



# ==============================================================================
# RODAPÉ
# ==============================================================================


st.divider()


st.caption(
    "🏆 Bolão Copa 2026 • FIFA PREMIUM VISUAL v3.2.1 • Motor Oficial v8.1"
)
