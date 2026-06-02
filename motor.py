# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# MOTOR OFICIAL v8.2
#
# Google Sheets Público → Motor → JSON → App
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
# GOOGLE SHEETS CSV
# ==============================================================================

def carregar_aba(nome):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(nome)}"
    )

    return pd.read_csv(url)



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

    print(f"✅ {nome} criado")



def numero(valor):

    try:
        if pd.isna(valor):
            return None

        return int(valor)

    except:
        return None



def converter_data(valor):

    try:

        return pd.to_datetime(
            valor,
            dayfirst=True
        )

    except:

        return pd.Timestamp.max



# ==============================================================================
# ITEM 4.1 - PONTOS POR JOGO
# ==============================================================================

def calcular_pontos_jogo(
    real_a,
    real_b,
    palp_a,
    palp_b
):

    ra = numero(real_a)
    rb = numero(real_b)
    pa = numero(palp_a)
    pb = numero(palp_b)


    if None in [
        ra,
        rb,
        pa,
        pb
    ]:

        return 0


    # Placar exato

    if ra == pa and rb == pb:

        return 12


    resultado_real = (
        "A"
        if ra > rb
        else "B"
        if rb > ra
        else "E"
    )


    resultado_palpite = (
        "A"
        if pa > pb
        else "B"
        if pb > pa
        else "E"
    )


    if resultado_real == resultado_palpite:


        if ra == pa or rb == pb:

            return 8


        return 5



    if ra == pa or rb == pb:

        return 2


    return 0



# ==============================================================================
# MOTOR PRINCIPAL
# ==============================================================================

def rodar_motor():


    print("🏆 Rodando Motor v8.2")


    # --------------------------------------------------------------------------
    # LEITURA DAS PLANILHAS
    # --------------------------------------------------------------------------


    participantes = carregar_aba(
        "C_Participantes"
    )


    jogos = carregar_aba(
        "C_Placares Oficiais"
    )


    palpites = carregar_aba(
        "C_Palpites"
    )



    # limpeza nomes

    participantes.columns = participantes.columns.str.strip()
    jogos.columns = jogos.columns.str.strip()
    palpites.columns = palpites.columns.str.strip()



    # --------------------------------------------------------------------------
    # PARTICIPANTES
    # --------------------------------------------------------------------------


    salvar_json(
        "participantes.json",
        participantes.to_dict(
            orient="records"
        )
    )



    # --------------------------------------------------------------------------
    # PALPITES
    # --------------------------------------------------------------------------


    salvar_json(
        "palpites.json",
        palpites.to_dict(
            orient="records"
        )
    )



    # --------------------------------------------------------------------------
    # JOGOS
    # --------------------------------------------------------------------------


    salvar_json(
        "jogos.json",
        jogos.to_dict(
            orient="records"
        )
    )



    # --------------------------------------------------------------------------
    # NORMALIZAÇÃO DOS PALPITES
    # --------------------------------------------------------------------------


    chave_jogo = (

        "ID_Jogo"

        if "ID_Jogo" in palpites.columns

        else

        "Jogo"

    )


    palpites_longos = palpites.melt(

        id_vars=[
            chave_jogo
        ],

        var_name="Participante",

        value_name="Palpite"

    )



    # --------------------------------------------------------------------------
    # RANKING
    # --------------------------------------------------------------------------


    ranking = []


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


        # Só entra no ranking quem enviou

        if envio == pd.Timestamp.max:

            continue



        pontos_grupo = 0



        meus = palpites_longos[

            palpites_longos["Participante"]
            .astype(str)
            .str.strip()

            == nome

        ]



        for _, linha in meus.iterrows():


            jogo = jogos[

                jogos[chave_jogo]

                == linha[chave_jogo]

            ]


            if jogo.empty:

                continue



            try:

                j = jogo.iloc[0]


                a,b = (

                    str(
                        linha["Palpite"]
                    )
                    .lower()
                    .split("x")

                )


                pontos_grupo += calcular_pontos_jogo(

                    j.get("Gols A"),

                    j.get("Gols B"),

                    a,

                    b

                )


            except:

                pass



        ranking.append(

            {

                "Participante": nome,


                "ITEM 4.1. Fase de Grupo":
                    pontos_grupo,


                "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias":
                    0,


                "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º":
                    0,


                "4.2. Artilheiro":
                    0,


                "TOTAL":
                    pontos_grupo,


                "Acertou_Campeao":
                    0,


                "Acertou_Artilheiro":
                    0,


                "Pontos_Eliminatorias":
                    0,


                "_Envio":
                    envio

            }

        )



    ranking = pd.DataFrame(
        ranking
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
            len(ranking)+1
        )

    )



    salvar_json(

        "ranking_geral.json",

        ranking.drop(
            columns=["_Envio"]
        )
        .to_dict(
            orient="records"
        )

    )



    salvar_json(

        "ranking_fase_grupos.json",

        ranking[
            [
                "posição",
                "Participante",
                "ITEM 4.1. Fase de Grupo",
                "TOTAL"
            ]
        ]
        .to_dict(
            orient="records"
        )

    )



    # --------------------------------------------------------------------------
    # PREMIAÇÃO
    # --------------------------------------------------------------------------


    total = len(participantes) * COTA


    salvar_json(

        "premiacao.json",

        {

            "Participantes":
                len(participantes),


            "Cota Individual":
                COTA,


            "Total Arrecadado":
                total,


            "Podio Geral":
                ranking.head(3)
                .drop(columns=["_Envio"])
                .to_dict(
                    orient="records"
                ),

            "Podio Fase Grupo":
                []

        }

    )



    # --------------------------------------------------------------------------
    # ESTATÍSTICAS
    # --------------------------------------------------------------------------


    realizados = (

        jogos[
            jogos["Gols A"]
            .notna()
        ]

        .shape[0]

    )


    salvar_json(

        "estatisticas_bolao.json",

        {

            "Participantes":
                len(participantes),


            "Jogos":
                f"{realizados}/{len(jogos)}",


            "Cota":
                COTA,


            "Arrecadado":
                total,


            "Lider":

                ranking.iloc[0]["Participante"]

                if len(ranking)

                else ""

        }

    )



    print(
        "🏆 MOTOR v8.2 FINALIZADO"
    )



# ==============================================================================
# EXECUTAR
# ==============================================================================

if __name__ == "__main__":

    rodar_motor()
