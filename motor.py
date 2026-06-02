# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# MOTOR OFICIAL v8.2.1
#
# Google Sheets Público → Motor → JSON → App
#
# O APP NÃO CALCULA NADA
# ==============================================================================


import pandas as pd
import json
from urllib.parse import quote


# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================


SHEET_ID = "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"

COTA = 200



# ==============================================================================
# LEITURA GOOGLE SHEETS
# ==============================================================================


def carregar_aba(nome):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(nome)}"
    )


    return pd.read_csv(
        url
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
            indent=4,
            default=str
        )


    print(
        f"✅ {nome}"
    )



def converter_data(valor):


    try:


        if pd.isna(valor):

            return pd.Timestamp.max


        if str(valor).strip() == "":

            return pd.Timestamp.max



        return pd.to_datetime(

            str(valor).strip(),

            dayfirst=True

        )


    except:


        return pd.Timestamp.max



# ==============================================================================
# ITEM 4.1 - PONTUAÇÃO FUTURA
# ==============================================================================


def calcular_pontos_jogo(
    real_a,
    real_b,
    palp_a,
    palp_b
):


    try:

        real_a = int(real_a)
        real_b = int(real_b)

        palp_a = int(palp_a)
        palp_b = int(palp_b)


    except:


        return 0



    if real_a == palp_a and real_b == palp_b:

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


        if real_a == palp_a or real_b == palp_b:

            return 8


        return 5



    if real_a == palp_a or real_b == palp_b:

        return 2



    return 0



# ==============================================================================
# MOTOR PRINCIPAL
# ==============================================================================


def rodar_motor():


    print(
        "🏆 Rodando Motor v8.2.1"
    )



    # ==========================================================================
    # CARREGAMENTO
    # ==========================================================================


    participantes = carregar_aba(
        "C_Participantes"
    )


    jogos = carregar_aba(
        "C_Placares Oficiais"
    )


    palpites = carregar_aba(
        "C_Palpites"
    )



    participantes.columns = participantes.columns.str.strip()

    jogos.columns = jogos.columns.str.strip()

    palpites.columns = palpites.columns.str.strip()



    # ==========================================================================
    # JSONS BASE
    # ==========================================================================


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



    # ==========================================================================
    # RANKING
    # ==========================================================================


    ranking_lista = []



    for _, pessoa in participantes.iterrows():



        nome = (

            str(
                pessoa.get(
                    "Participantes",
                    ""
                )
            )

            .strip()

        )



        envio = converter_data(

            pessoa.get(

                "Data e hora do Palpite"

            )

        )



        # Somente quem enviou palpite entra

        if envio == pd.Timestamp.max:

            continue



        pontos_grupo = 0

        pontos_eliminatorias = 0

        pontos_classificacao = 0

        pontos_artilheiro = 0



        total = (

            pontos_grupo

            +

            pontos_eliminatorias

            +

            pontos_classificacao

            +

            pontos_artilheiro

        )



        ranking_lista.append(

            {

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

                    0,


                "Acertou_Artilheiro":

                    0,


                "Pontos_Eliminatorias":

                    pontos_eliminatorias,


                "_Envio":

                    envio

            }

        )



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

        "posição",

        range(

            1,

            len(ranking) + 1

        )

    )



    ranking_publico = ranking.drop(

        columns=[

            "Acertou_Campeao",

            "Acertou_Artilheiro",

            "Pontos_Eliminatorias",

            "_Envio"

        ]

    )



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

                "posição",

                "Participante",

                "ITEM 4.1. Fase de Grupo"

            ]

        ].to_dict(
            orient="records"
        )

    )



    # ==========================================================================
    # PREMIAÇÃO
    # ==========================================================================


    arrecadado = (

        len(participantes)

        *

        COTA

    )



    salvar_json(

        "premiacao.json",

        {

            "Valores Arrecadados":

            {

                "Participantes":

                    len(participantes),


                "Cota":

                    COTA,


                "Total":

                    arrecadado

            },


            "Podio Geral":

                ranking_publico.head(3)

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



    # ==========================================================================
    # ESTATÍSTICAS
    # ==========================================================================


    jogos_realizados = 0


    salvar_json(

        "estatisticas_bolao.json",

        {

            "Participantes":

                len(participantes),


            "Jogos":

                f"{jogos_realizados}/{len(jogos)}",


            "Cota":

                COTA,


            "Arrecadado":

                arrecadado,


            "Lider":

                ranking_publico.iloc[0]["Participante"]

                if len(ranking_publico)

                else "-"

        }

    )



    salvar_json(

        "auditoria.json",

        ranking.to_dict(
            orient="records"
        )

    )



    print(
        "🏆 MOTOR v8.2.1 FINALIZADO COM SUCESSO"
    )



# ==============================================================================
# EXECUÇÃO
# ==============================================================================


if __name__ == "__main__":

    rodar_motor()
