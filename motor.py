# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# MOTOR OFICIAL v7.1
#
# Google Sheets → Motor → JSON → Streamlit
#
# Fonte única:
# C_Participantes
# C_Placares Oficiais
# C_Palpites
#
# ==============================================================================


import pandas as pd
import json
import os
import gspread
from google.oauth2.service_account import Credentials


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================


SHEET_ID = "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"

COTA = 200


# ==============================================================================
# GOOGLE SHEETS
# ==============================================================================


def conectar_google():

    credenciais = json.loads(
        os.environ["GOOGLE_CREDENTIALS"]
    )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]


    creds = Credentials.from_service_account_info(
        credenciais,
        scopes=scopes
    )


    cliente = gspread.authorize(
        creds
    )


    return cliente.open_by_key(
        SHEET_ID
    )



# ==============================================================================
# UTILIDADES
# ==============================================================================


def salvar_json(nome, dados):

    with open(
        nome,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"✅ Gerado: {nome}"
    )



def numero(valor):

    try:
        return int(valor)

    except:
        return None



def data(valor):

    try:

        return pd.to_datetime(
            valor,
            dayfirst=True
        )

    except:

        return pd.Timestamp.max



# ==============================================================================
# ITEM 4.1 - PLACARES
# ==============================================================================


def calcular_pontos_jogo(
    real_a,
    real_b,
    palp_a,
    palp_b
):


    real_a = numero(real_a)
    real_b = numero(real_b)
    palp_a = numero(palp_a)
    palp_b = numero(palp_b)


    if None in [
        real_a,
        real_b,
        palp_a,
        palp_b
    ]:
        return 0



    if (
        real_a == palp_a
        and
        real_b == palp_b
    ):

        return 12



    resultado_real = (
        "A"
        if real_a > real_b
        else
        "B"
        if real_b > real_a
        else
        "E"
    )


    resultado_palpite = (
        "A"
        if palp_a > palp_b
        else
        "B"
        if palp_b > palp_a
        else
        "E"
    )



    if resultado_real == resultado_palpite:


        if (
            real_a == palp_a
            or
            real_b == palp_b
        ):

            return 8


        return 5



    if (
        real_a == palp_a
        or
        real_b == palp_b
    ):

        return 2



    return 0



# ==============================================================================
# MOTOR
# ==============================================================================


def rodar_motor():


    print("="*80)
    print("🏆 MOTOR v7.1 INICIADO")
    print("="*80)



    sheet = conectar_google()



    participantes = pd.DataFrame(
        sheet
        .worksheet("C_Participantes")
        .get_all_records()
    )


    jogos = pd.DataFrame(
        sheet
        .worksheet("C_Placares Oficiais")
        .get_all_records()
    )


    palpites = pd.DataFrame(
        sheet
        .worksheet("C_Palpites")
        .get_all_records()
    )



# ==============================================================================
# NORMALIZAÇÃO DOS PALPITES
# ==============================================================================


    if "ID_Jogo" in palpites.columns:


        palpites_longos = palpites.melt(

            id_vars=[
                "ID_Jogo"
            ],


            var_name=
                "Participante",


            value_name=
                "Palpite"

        )


    else:


        palpites_longos = pd.DataFrame()



# ==============================================================================
# RANKING
# ==============================================================================


    ranking = []



    for _, pessoa in participantes.iterrows():


        nome = pessoa[
            "Participantes"
        ]


        pontos_grupo = 0


        pontos_eliminatorias = 0


        pontos_classificacao = 0


        pontos_artilheiro = 0


        acertou_campeao = 0



        # =====================================================
        # ITEM 4.1
        # =====================================================


        meus_palpites = palpites_longos[

            palpites_longos["Participante"]
            ==
            nome

        ]



        for _, palpite in meus_palpites.iterrows():



            jogo = jogos[

                jogos["ID_Jogo"]
                ==
                palpite["ID_Jogo"]

            ]



            if jogo.empty:

                continue



            jogo = jogo.iloc[0]



            # aqui considera formato:
            # "2x1"


            try:


                ga,gb = (

                    str(
                        palpite["Palpite"]
                    )
                    .lower()
                    .split("x")

                )


                pontos_grupo += calcular_pontos_jogo(


                    jogo.get(
                        "Gols A"
                    ),


                    jogo.get(
                        "Gols B"
                    ),


                    ga,

                    gb

                )


            except:


                pass



        # =====================================================
        # TOTAL
        # =====================================================


        total = (

            pontos_grupo
            +
            pontos_eliminatorias
            +
            pontos_classificacao
            +
            pontos_artilheiro

        )



        ranking.append({


            "Participante":
                nome,


            "ITEM 4.1. Fase de Grupo":
                pontos_grupo,


            "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias":
                pontos_eliminatorias,


            "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º":
                pontos_classificacao,


            "4.2. Artilheiro":
                pontos_artilheiro,


            "TOTAL":
                total,


            "_Campeao":
                acertou_campeao,


            "_Artilheiro":
                1 if pontos_artilheiro else 0,


            "_Envio":
                data(
                    pessoa.get(
                        "Data e hora do Palpite"
                    )
                )

        })



# ==============================================================================
# DESEMPATE
# ==============================================================================


    ranking = pd.DataFrame(
        ranking
    )


    ranking = ranking.sort_values(

        by=[

            "TOTAL",

            "_Campeao",

            "_Artilheiro",

            "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias",

            "_Envio"

        ],


        ascending=[

            False,
            False,
            False,
            False,
            True

        ]

    )



    ranking.insert(

        0,

        "Posição",

        range(
            1,
            len(ranking)+1
        )

    )



    ranking_publico = ranking.drop(

        columns=[

            "_Campeao",

            "_Artilheiro",

            "_Envio"

        ]

    )



# ==============================================================================
# JSONS
# ==============================================================================


    salvar_json(

        "ranking_geral.json",

        ranking_publico.to_dict(
            orient="records"
        )

    )



    salvar_json(

        "ranking_fase_grupos.json",

        ranking_publico[
            [
                "Posição",
                "Participante",
                "ITEM 4.1. Fase de Grupo"
            ]
        ].to_dict(
            orient="records"
        )

    )



    salvar_json(

        "jogos.json",

        jogos.to_dict(
            orient="records"
        )

    )



    salvar_json(

        "palpites.json",

        palpites.to_dict(
            orient="records"
        )

    )



    total = (
        len(participantes)
        *
        COTA
    )



    salvar_json(

        "estatisticas_bolao.json",

        {

            "Participantes":
                len(participantes),

            "Cota":
                COTA,

            "Arrecadado":
                total,

            "Premiação Geral":
                total * 0.80,

            "Premiação Fase Grupos":
                total * 0.20

        }

    )



    salvar_json(

        "premiacao.json",

        {

            "Podio Geral":

                ranking_publico
                .head(3)
                .to_dict(
                    orient="records"
                )


        }

    )



    print("="*80)
    print("🏆 MOTOR v7.1 FINALIZADO")
    print("✅ JSONS ATUALIZADOS")
    print("="*80)



# ==============================================================================
# EXECUÇÃO
# ==============================================================================


if __name__ == "__main__":

    rodar_motor()
