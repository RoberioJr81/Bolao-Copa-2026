# ==============================================================================
# 🔍 BOLÃO COPA 2026
# APP DE AUDITORIA DO FLUXO
#
# Google Sheets → motor.py → JSON → app.py
# ==============================================================================

import streamlit as st
import pandas as pd
import json
import os
import traceback


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Auditoria Bolão 2026",
    page_icon="🔍",
    layout="wide"
)


st.title("🔍 Auditoria do Sistema Bolão Copa 2026")

st.write(
    "Verificando fluxo: Google Sheets → motor.py → JSON → app.py"
)

st.divider()


# ==============================================================================
# 1. TESTE EXISTÊNCIA DO MOTOR
# ==============================================================================

st.header("1️⃣ Verificação do motor.py")


if os.path.exists("motor.py"):

    st.success(
        "✅ Arquivo motor.py encontrado"
    )


else:

    st.error(
        "❌ motor.py NÃO encontrado"
    )



# ==============================================================================
# 2. EXECUÇÃO DO MOTOR
# ==============================================================================

st.header("2️⃣ Execução do Motor")


try:

    from motor import rodar_motor


    st.info(
        "Executando rodar_motor()..."
    )


    rodar_motor()


    st.success(
        "✅ Motor executado sem erro"
    )


except Exception as erro:


    st.error(
        "❌ Erro durante execução do motor"
    )


    st.code(
        str(erro)
    )


    st.code(
        traceback.format_exc()
    )



st.divider()



# ==============================================================================
# 3. AUDITORIA DOS JSONS
# ==============================================================================

st.header("3️⃣ Verificação dos JSONs")


arquivos_json = [

    "ranking_geral.json",

    "ranking_fase_grupos.json",

    "participantes.json",

    "jogos.json",

    "palpites.json",

    "premiacao.json",

    "estatisticas_bolao.json",

    "auditoria.json"

]


resultado = []


for arquivo in arquivos_json:


    existe = os.path.exists(
        arquivo
    )


    tamanho = (

        os.path.getsize(
            arquivo
        )

        if existe

        else

        0

    )


    resultado.append(

        {

            "Arquivo": arquivo,

            "Existe": existe,

            "Tamanho bytes": tamanho

        }

    )


st.dataframe(

    pd.DataFrame(resultado),

    width="stretch"

)



st.divider()



# ==============================================================================
# 4. CONTEÚDO DOS JSONS
# ==============================================================================

st.header("4️⃣ Amostra do conteúdo gerado")


for arquivo in arquivos_json:


    st.subheader(
        arquivo
    )


    if os.path.exists(
        arquivo
    ):


        try:


            with open(
                arquivo,
                "r",
                encoding="utf-8"
            ) as f:


                dados = json.load(
                    f
                )


            st.write(
                "Tipo:",
                type(dados).__name__
            )


            if isinstance(
                dados,
                list
            ):


                st.write(
                    "Quantidade registros:",
                    len(dados)
                )


                st.json(
                    dados[:2]
                )


            elif isinstance(
                dados,
                dict
            ):


                st.json(
                    dados
                )


        except Exception as erro:


            st.error(
                erro
            )


    else:


        st.warning(
            "Arquivo não encontrado"
        )



st.divider()



# ==============================================================================
# 5. TESTE RÁPIDO DO RESULTADO ESPERADO
# ==============================================================================

st.header("5️⃣ Resultado esperado do Bolão")


def abrir(nome, padrao):

    try:

        with open(
            nome,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return padrao



estatisticas = abrir(

    "estatisticas_bolao.json",

    {}

)


ranking = abrir(

    "ranking_geral.json",

    []

)


c1,c2,c3,c4 = st.columns(4)


c1.metric(

    "Participantes",

    estatisticas.get(
        "Participantes",
        "ERRO"
    )

)


c2.metric(

    "Jogos",

    estatisticas.get(
        "Jogos",
        "ERRO"
    )

)


c3.metric(

    "Arrecadado",

    estatisticas.get(
        "Arrecadado",
        "ERRO"
    )

)


lider = (

    ranking[0]["Participante"]

    if ranking

    else

    "SEM RANKING"

)


c4.metric(

    "Líder",

    lider

)


st.divider()


st.caption(
    "🔍 Auditoria Motor v8.1 / JSON / App"
)
