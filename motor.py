# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# MOTOR OFICIAL v8.1 CONSOLIDADO
#
# Google Sheets → Motor → JSON → App
#
# O app.py NÃO calcula nada.
# ==============================================================================

import pandas as pd
import json
import os
import gspread
from google.oauth2.service_account import Credentials


# ==============================================================================
# CONFIGURAÇÕES
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

    return gspread.authorize(
        creds
    ).open_by_key(
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

    print(f"✅ {nome} atualizado")


def inteiro(valor):

    try:
        return int(valor)

    except:
        return None


def converter_data(valor):

    try:

        if str(valor).strip() == "":
            return pd.Timestamp.max

        return pd.to_datetime(
            valor,
            dayfirst=True
        )

    except:

        return pd.Timestamp.max


# ==============================================================================
# REGRA ITEM 4.1
# ==============================================================================

def calcular_pontos_jogo(
    real_a,
    real_b,
    palp_a,
    palp_b
):

    ra = inteiro(real_a)
    rb = inteiro(real_b)

    pa = inteiro(palp_a)
    pb = inteiro(palp_b)


    if None in [ra, rb, pa, pb]:

        return 0


    # Placar exato

    if ra == pa and rb == pb:

        return 12


    resultado_real = (
        "A"
        if ra > rb
        else
        "B"
        if rb > ra
        else
        "E"
    )


    resultado_palpite = (
        "A"
        if pa > pb
        else
        "B"
        if pb > pa
        else
        "E"
    )


    # Resultado + gols de uma seleção

    if resultado_real == resultado_palpite:

        if ra == pa or rb == pb:

            return 8

        return 5


    # Gol de uma seleção

    if ra == pa or rb == pb:

        return 2


    return 0


# ==============================================================================
# MOTOR
# ==============================================================================

def rodar_motor():


    print("="*80)
    print("🏆 MOTOR v8.1")
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


    # ======================================================================
    # ESTATÍSTICAS
    # ======================================================================


    total_participantes = len(
        participantes
    )


    jogos_realizados = jogos[

        (jogos["Gols A"].astype(str) != "")

        &

        (jogos["Gols B"].astype(str) != "")

    ].shape[0]


    total_jogos = len(jogos)



    # ======================================================================
    # PARTICIPANTES DO RANKING
    # ======================================================================


    ranking_lista = []


    concorrentes = participantes[

        participantes[
            "Data e hora do Palpite"
        ].astype(str).str.strip() != ""

    ]



    for _, pessoa in concorrentes.iterrows():


        nome = pessoa[
            "Participantes"
        ]


        # módulos futuros calculáveis

        pontos_grupo = 0

        pontos_eliminatorias = 0

        pontos_classificacao = 0

        pontos_artilheiro = 0


        acertou_campeao = 0

        acertou_artilheiro = 0


        total = (

            pontos_grupo

            +

            pontos_eliminatorias

            +

            pontos_classificacao

            +

            pontos_artilheiro

        )


        ranking_lista.append({


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


            "Acertou_Campeao":
                acertou_campeao,


            "Acertou_Artilheiro":
                acertou_artilheiro,


            "Pontos_Eliminatorias":
                pontos_eliminatorias,


            "_Envio":
                converter_data(
                    pessoa.get(
                        "Data e hora do Palpite"
                    )
                )

        })


    ranking = pd.DataFrame(
        ranking_lista
    )


    ranking = ranking.sort_values(

        by=[

            "TOTAL",

            "Acertou_Campeao",

            "Acertou_Artilheiro",

            "Pontos_Eliminatorias",

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


    auditoria = ranking.copy()


    ranking_publico = ranking.drop(

        columns=[

            "Acertou_Campeao",

            "Acertou_Artilheiro",

            "Pontos_Eliminatorias",

            "_Envio"

        ]

    )


    # ======================================================================
    # JSONS OFICIAIS
    # ======================================================================


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

        "participantes.json",

        participantes.to_dict(
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


    arrecadado = (
        total_participantes
        *
        COTA
    )


    salvar_json(

        "estatisticas_bolao.json",

        {

            "Participantes":
                total_participantes,


            "Jogos":
                f"{jogos_realizados}/{total_jogos}",


            "Cota":
                COTA,


            "Arrecadado":
                arrecadado

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
                ),


            "Podio Fase Grupo":

                ranking_publico
                .sort_values(
                    by="ITEM 4.1. Fase de Grupo",
                    ascending=False
                )
                .head(3)
                .to_dict(
                    orient="records"
                )

        }

    )


    auditoria["_Envio"] = (

        auditoria["_Envio"]
        .astype(str)

    )


    salvar_json(

        "auditoria.json",

        auditoria.to_dict(
            orient="records"
        )

    )


    print("="*80)
    print("🏆 MOTOR v8.1 FINALIZADO")
    print("✅ Ranking oficial")
    print("✅ JSONs congelados")
    print("="*80)


# ==============================================================================
# EXECUTAR
# ==============================================================================


if __name__ == "__main__":

    rodar_motor()
