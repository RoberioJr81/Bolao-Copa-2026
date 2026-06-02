# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.4
# MOTOR v6.0 INTEGRADO
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
# EXECUTA MOTOR OFICIAL
# ============================================================

try:

    from motor import executar_motor


    with st.spinner(
        "Atualizando dados oficiais do bolão..."
    ):

        executar_motor()


except Exception as erro:

    st.warning(
        f"Motor não executado: {erro}"
    )



# ============================================================
# CARREGADOR JSON
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



# ============================================================
# DADOS
# ============================================================

ranking = carregar_json(
    "ranking_geral.json"
)

jogos = carregar_json(
    "jogos.json"
)

palpites = carregar_json(
    "palpites.json"
)



# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .titulo {
        text-align:center;
        font-size:42px;
        font-weight:bold;
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
    Sistema Oficial • Motor v6.0 • FIFA Premium
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()



# ============================================================
# VALIDAÇÃO
# ============================================================

if ranking.empty:

    st.error(
        "Ranking não encontrado."
    )

    st.stop()



# ============================================================
# PAINEL SUPERIOR
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
    "Teto",
    "1797 pts"
)


lider = ranking.iloc[0]


c4.metric(
    "Líder",
    lider["Participantes"]
)



st.divider()



# ============================================================
# ABAS
# ============================================================

aba_inicio, aba_rank, aba_premio, aba_jogos, aba_regra = st.tabs(

    [

        "Início",

        "Classificação Geral",

        "Premiação",

        "Jogos e Palpites",

        "Regulamento"

    ]

)



# ============================================================
# INÍCIO
# ============================================================

with aba_inicio:


    st.success(
        "Bolão atualizado automaticamente pelo motor oficial."
    )


    st.write(
        "Últimos dados sincronizados diretamente do Google Sheets."
    )



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with aba_rank:


    st.header(
        "Classificação Geral"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        width="stretch"

    )



# ============================================================
# PREMIAÇÃO
# ============================================================

with aba_premio:


    st.header(
        "Premiação Oficial"
    )


    st.subheader(
        "Fase de Grupos - 20%"
    )


    st.write(
        """
        1º colocado: 50%

        2º colocado: 30%

        3º colocado: 20%
        """
    )


    st.subheader(
        "Premiação Geral - 80%"
    )


    st.write(
        """
        Campeão: 60%

        Vice: 25%

        Terceiro: 15%
        """
    )



# ============================================================
# JOGOS E PALPITES
# ============================================================

with aba_jogos:


    st.header(
        "Jogos e Palpites"
    )


    if jogos.empty or palpites.empty:


        st.warning(
            "Palpites ainda não disponíveis."
        )


    else:


        lista_jogos = jogos[

            "id_jogo"

        ].tolist()



        jogo_escolhido = st.selectbox(

            "Selecione o jogo",

            lista_jogos

        )



        jogo = jogos[

            jogos["id_jogo"]

            ==

            jogo_escolhido

        ].iloc[0]



        st.subheader(

            f'{jogo["Seleção A"]} x {jogo["Seleção B"]}'

        )


        st.write(

            f'Placar oficial: {jogo["Gols A"]} x {jogo["Gols B"]}'

        )



        tabela = palpites[

            palpites["id_jogo"]

            ==

            jogo_escolhido

        ]



        st.dataframe(

            tabela,

            hide_index=True,

            width="stretch"

        )



# ============================================================
# REGULAMENTO
# ============================================================

with aba_regra:


    st.header(
        "Critérios Oficiais"
    )


    st.markdown(
        """

### Pontuação

12 pontos - placar exato  

8 pontos - vencedor + um placar  

5 pontos - vencedor/empate  

2 pontos - um placar correto  


### Desempate

1. Acerto do Campeão

2. Acerto do Artilheiro

3. Maior pontuação na fase eliminatória

4. Maior antecedência no envio


        """
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "Bolão Copa 2026 • Motor Oficial v6.0"
)
