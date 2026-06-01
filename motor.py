
# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# FIFA PREMIUM v3.0
# ============================================================

import pandas as pd
import os
import json
import traceback
from urllib.parse import quote


# ============================================================
# CONFIGURAÇÕES
# ============================================================

SHEET_ID = "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"

PASTA_PUBLICACAO = "publicacao"

TETO_MAXIMO = 1797


# ============================================================
# UTILITÁRIOS
# ============================================================

def exportar_json(nome, df):

    os.makedirs(
        PASTA_PUBLICACAO,
        exist_ok=True
    )

    caminho = os.path.join(
        PASTA_PUBLICACAO,
        nome
    )

    df.to_json(
        caminho,
        orient="records",
        force_ascii=False,
        indent=4
    )

    print(
        "✅ JSON:",
        nome
    )


# ============================================================
# GOOGLE SHEETS
# ============================================================

def carregar_aba(nome):

    url = (
        "https://docs.google.com/spreadsheets/d/"
        +
        SHEET_ID
        +
        "/gviz/tq?tqx=out:csv&sheet="
        +
        quote(nome)
    )

    return pd.read_csv(url)



def carregar_dados():

    print("🔄 Carregando Google Sheets")


    return {

        "participantes": carregar_aba(
            "C_Participantes"
        ),

        "oficiais": carregar_aba(
            "C_Placares Oficiais"
        ),

        "palpites": carregar_aba(
            "C_Palpites"
        )

    }


# ============================================================
# PREPARAR JOGOS
# ============================================================

def preparar_jogos(df):


    base = df.copy()


    base = base[

        (base["Partidas"].notna())

        &

        (base["Unnamed: 9"].notna())

    ].copy()


    base = base.reset_index(drop=True)


    jogos = pd.DataFrame()


    jogos["id_jogo"] = range(
        1,
        len(base)+1
    )


    jogos["Fase"] = "Grupo"


    jogos["Seleção A"] = base[
        "Partidas"
    ]


    jogos["Gols A"] = base[
        "Unnamed: 5"
    ]


    jogos["Gols B"] = base[
        "Unnamed: 7"
    ]


    jogos["Seleção B"] = base[
        "Unnamed: 9"
    ]


    return jogos.fillna("")


# ============================================================
# PREPARAR PALPITES
# ============================================================

def preparar_palpites(df):


    lista = []


    for _, linha in df.iterrows():


        participante = linha[
            "Participantes"
        ]


        jogo = 1


        for valor in linha.values:


            texto = str(valor).replace(
                " ",
                ""
            )


            if "x" in texto:


                try:


                    a,b = texto.split(
                        "x"
                    )


                    lista.append(

                        {

                            "Participante":
                            participante,

                            "id_jogo":
                            jogo,

                            "A":
                            int(a),

                            "B":
                            int(b)

                        }

                    )


                    jogo += 1


                except:


                    pass


    return pd.DataFrame(lista)



# ============================================================
# CALCULAR PLACARES
# ============================================================

def calcular_placares(jogos, palpites):


    saida = []


    for _, p in palpites.iterrows():


        jogo = jogos[

            jogos["id_jogo"]
            ==
            p["id_jogo"]

        ]


        if jogo.empty:

            continue


        jogo = jogo.iloc[0]


        pontos = 0


        try:


            oa = int(jogo["Gols A"])

            ob = int(jogo["Gols B"])


            if (
                p["A"] == oa
                and
                p["B"] == ob
            ):

                pontos = 12


            else:


                if (

                    (oa-ob > 0 and p["A"]-p["B"] > 0)

                    or

                    (oa-ob < 0 and p["A"]-p["B"] < 0)

                    or

                    (oa-ob == 0 and p["A"]-p["B"] == 0)

                ):

                    pontos = 5



        except:


            pontos = 0



        saida.append(

            {

                "Participante":
                p["Participante"],

                "Pontos":
                pontos

            }

        )


    return pd.DataFrame(saida)



# ============================================================
# RANKING
# ============================================================

def gerar_ranking(df):


    ranking = (

        df.groupby(
            "Participante",
            as_index=False
        )

        ["Pontos"]

        .sum()

    )


    ranking = ranking.rename(

        columns={

            "Pontos":"TOTAL"

        }

    )


    ranking = ranking.sort_values(

        "TOTAL",

        ascending=False

    )


    ranking.insert(

        0,

        "Posição",

        range(1,len(ranking)+1)

    )


    return ranking



# ============================================================
# MOTOR PRINCIPAL
# ============================================================

def executar_motor():


    print("="*80)
    print("🏆 MOTOR BOLÃO COPA 2026 — PRODUÇÃO")
    print("="*80)


    try:


        dados = carregar_dados()


        print("✅ Google Sheets conectado")


        jogos = preparar_jogos(
            dados["oficiais"]
        )


        print(
            "✅ Jogos:",
            len(jogos)
        )


        palpites = preparar_palpites(
            dados["palpites"]
        )


        print(
            "✅ Palpites:",
            len(palpites)
        )


        placares = calcular_placares(

            jogos,

            palpites

        )


        print(
            "✅ Pontuações:",
            len(placares)
        )


        ranking = gerar_ranking(
            placares
        )


        exportar_json(

            "ranking_geral.json",

            ranking

        )


        exportar_json(

            "jogos.json",

            jogos

        )


        print()
        print("🏆 MOTOR FINALIZADO COM SUCESSO")


        return True



    except Exception as erro:


        print("❌ ERRO NO MOTOR")

        print(erro)


        traceback.print_exc()


        return False



# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":


    executar_motor()
