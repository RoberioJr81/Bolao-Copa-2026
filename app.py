
import streamlit as st
import pandas as pd
import json


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Bolão Copa 2026",
    page_icon="🏆",
    layout="wide"
)


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    h1 {
        text-align: center;
        color: #0B3D91;
        font-size: 42px;
    }

    h2, h3 {
        color: #1F2937;
    }

    [data-testid="stMetricValue"] {
        font-size: 28px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNÇÕES
# ============================================================

def carregar_json(nome):

    with open(
        nome,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)


def tabela(dados):

    return pd.DataFrame(dados)



# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

ranking = tabela(
    carregar_json("ranking_geral.json")
)


fase_grupos = tabela(
    carregar_json("ranking_fase_grupos.json")
)


estatisticas = tabela(
    carregar_json("estatisticas_bolao.json")
)



# ============================================================
# CABEÇALHO
# ============================================================

st.title("🏆 Bolão Copa do Mundo 2026")


st.divider()



# ============================================================
# CARDS DE ESTATÍSTICAS
# ============================================================

st.subheader("📊 Estatísticas Gerais")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Participantes",
        int(estatisticas["Participantes"][0])
    )


with col2:
    st.metric(
        "Maior Pontuação",
        int(estatisticas["Maior Pontuação"][0])
    )


with col3:
    st.metric(
        "Média",
        round(
            float(estatisticas["Média Pontos"][0]),
            2
        )
    )


with col4:
    st.metric(
        "Teto Possível",
        "1797 pts"
    )


st.info(
    "👑 Líder(es): "
    + str(estatisticas["Líder(es)"][0])
)



# ============================================================
# RANKING GERAL
# ============================================================

st.divider()


st.subheader("🏆 Classificação Geral")


st.dataframe(
    ranking,
    hide_index=True,
    use_container_width=True
)



# ============================================================
# PREMIAÇÃO FASE DE GRUPOS
# ============================================================

st.divider()


st.subheader("🥇 Premiação da Fase de Grupos")


st.dataframe(
    fase_grupos,
    hide_index=True,
    use_container_width=True
)



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "Sistema Bolão Copa 2026 • Atualização automática via Render"
)
