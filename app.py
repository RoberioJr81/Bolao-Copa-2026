# ============================================================
# APP BOLÃO COPA 2026
# FIFA PREMIUM VISUAL v1.6
# COMPATÍVEL COM MOTOR OFICIAL v6.2
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
# EXECUTA MOTOR
# ============================================================

try:

    from motor import executar_motor

    with st.spinner(
        "Atualizando dados oficiais..."
    ):

        executar_motor()

except Exception as erro:

    st.warning(
        f"Motor não executado: {erro}"
    )


# ============================================================
# CARREGAR JSON
# ============================================================

def carregar(nome):

    caminho=os.path.join(
        BASE_DIR,
        nome
    )

    if os.path.exists(caminho):

        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as f:

            return pd.DataFrame(
                json.load(f)
            )

    return pd.DataFrame()



ranking = carregar(
    "ranking_geral.json"
)

ranking_grupos = carregar(
    "ranking_fase_grupos.json"
)

jogos = carregar(
    "jogos.json"
)

palpites = carregar(
    "matriz_palpites.json"
)



# ============================================================
# VISUAL
# ============================================================

st.markdown(
"""
<style>

.titulo{
text-align:center;
font-size:44px;
font-weight:900;
color:#006b2e;
}

.subtitulo{
text-align:center;
font-size:16px;
color:#555;
}

.podio{
border-radius:15px;
padding:20px;
background:#f7f7f7;
text-align:center;
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
<div class='titulo'>
🏆 Bolão Copa do Mundo 2026
</div>
""",
unsafe_allow_html=True
)


st.markdown(
"""
<div class='subtitulo'>
Sistema Oficial • FIFA Premium • Motor v6.2
</div>
""",
unsafe_allow_html=True
)


st.divider()



# ============================================================
# PROTEÇÃO
# ============================================================

if ranking.empty:

    st.error(
        "Ranking indisponível."
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
    "Teto máximo",
    "1797 pontos"
)


c4.metric(
    "Líder",
    ranking.iloc[0]["Participantes"]
)



st.divider()



# ============================================================
# ABAS
# ============================================================

aba_inicio, aba_ranking, aba_premios, aba_jogos, aba_palpites, aba_regra = st.tabs(

[
"🏠 Início",
"🏆 Classificação",
"🏅 Premiação",
"⚽ Jogos",
"📋 Palpites",
"📜 Regulamento"
]

)



# ============================================================
# INÍCIO
# ============================================================

with aba_inicio:


    st.header(
        "Sistema Oficial do Bolão"
    )


    st.success(
        "Atualização automática pelo Google Sheets ativa."
    )


    st.write(
        """
        O ranking é atualizado conforme:
        
        1. Pontuação total  
        2. Acerto do campeão  
        3. Acerto do artilheiro  
        4. Fase eliminatória  
        5. Ordem oficial de envio
        """
    )



# ============================================================
# CLASSIFICAÇÃO
# ============================================================

with aba_ranking:


    st.header(
        "🏆 Classificação Geral"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        use_container_width=True

    )


    st.subheader(
        "⚽ Ranking da Fase de Grupos"
    )


    if not ranking_grupos.empty:

        st.dataframe(

            ranking_grupos,

            hide_index=True,

            use_container_width=True

        )



# ============================================================
# PREMIAÇÃO
# ============================================================

with aba_premios:


    st.header(
        "🏅 Premiação Oficial"
    )


    st.subheader(
        "🏆 Geral"
    )


    c1,c2,c3 = st.columns(3)


    top = ranking.head(3)


    medalhas=[

        "🥇 Campeão",

        "🥈 Vice",

        "🥉 Terceiro"

    ]


    colunas=[
        c1,
        c2,
        c3
    ]


    for i in range(
        min(3,len(top))
    ):

        with colunas[i]:

            st.markdown(
                f"### {medalhas[i]}"
            )

            st.metric(

                top.iloc[i]["Participantes"],

                str(
                    int(top.iloc[i]["TOTAL"])
                )
                +
                " pontos"

            )



    st.divider()


    st.subheader(
        "⚽ Fase de Grupos"
    )


    if not ranking_grupos.empty:


        topg = ranking_grupos.head(3)


        g1,g2,g3 = st.columns(3)


        for i,col in enumerate(
            [g1,g2,g3]
        ):

            if i < len(topg):

                with col:

                    st.markdown(
                        f"### {medalhas[i]}"
                    )


                    st.metric(

                        topg.iloc[i]["Participantes"],

                        str(
                            int(
                                topg.iloc[i]["Fase de Grupo"]
                            )
                        )
                        +
                        " pontos"

                    )



# ============================================================
# JOGOS
# ============================================================

with aba_jogos:


    st.header(
        "⚽ Tabela Completa de Jogos"
    )


    if not jogos.empty:


        ordem=[

            "Jogo",

            "Seleção A",

            "Placar A",

            "Placar B",

            "Seleção B"

        ]


        existentes=[

            c for c in ordem

            if c in jogos.columns

        ]


        st.dataframe(

            jogos[existentes],

            hide_index=True,

            use_container_width=True

        )



# ============================================================
# PALPITES
# ============================================================

with aba_palpites:


    st.header(
        "📋 Mapa Geral de Palpites"
    )


    st.caption(
        "Placar Oficial seguido pelos participantes na ordem oficial."
    )


    if palpites.empty:


        st.warning(
            "Palpites ainda não disponíveis."
        )


    else:


        st.dataframe(

            palpites,

            hide_index=True,

            use_container_width=True

        )



# ============================================================
# REGULAMENTO
# ============================================================

with aba_regra:


    st.header(
        "📜 Regulamento Oficial"
    )


    st.markdown(
"""

### Pontuação dos jogos

🏆 **12 pontos**
- placar exato


⭐ **8 pontos**
- vencedor + gols de uma seleção


✔ **5 pontos**
- vencedor correto


➕ **2 pontos**
- gols de uma seleção


---

### Critérios de desempate

1. Acerto do campeão

2. Acerto do artilheiro

3. Pontuação fase eliminatória

4. Maior antecedência de envio


"""
    )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()


st.caption(
    "Bolão Copa 2026 • Motor v6.2 • FIFA Premium"
)
