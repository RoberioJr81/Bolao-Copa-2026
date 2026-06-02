# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v6.0 — REGULAMENTO FINAL
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

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TETO_MAXIMO = 1797


# ============================================================
# GOOGLE SHEETS
# ============================================================

def carregar_aba(nome):

    url = (
        "https://docs.google.com/spreadsheets/d/"
        + SHEET_ID
        + "/gviz/tq?tqx=out:csv&sheet="
        + quote(nome)
    )

    return pd.read_csv(url)



def carregar_dados():

    print("🔄 Carregando Google Sheets")

    return {

        "jogos":
            carregar_aba("C_Placares Oficiais"),

        "palpites":
            carregar_aba("C_Palpites"),

        "participantes":
            carregar_aba("C_Participantes")

    }


# ============================================================
# EXPORTAÇÃO JSON
# ============================================================

def exportar_json(nome, df):

    caminho = os.path.join(
        BASE_DIR,
        nome
    )

    df.to_json(
        caminho,
        orient="records",
        force_ascii=False,
        indent=4
    )

    print(
        "✅ JSON criado:",
        nome
    )


# ============================================================
# JOGOS OFICIAIS
# ============================================================

def preparar_jogos(df):

    print("🔄 Preparando jogos")


    base = df[

        df.iloc[:,0].notna()

        &

        df.iloc[:,1].notna()

        &

        df.iloc[:,2].notna()

        &

        df["Partidas"].notna()

        &

        df["Unnamed: 9"].notna()

    ].copy()


    base = base.reset_index(
        drop=True
    )


    jogos = pd.DataFrame()


    jogos["id_jogo"] = range(
        1,
        len(base)+1
    )


    jogos["Status"] = base.iloc[:,0]

    jogos["Data"] = base.iloc[:,1]

    jogos["Sede"] = base.iloc[:,2]

    jogos["Seleção A"] = base["Partidas"]

    jogos["Gols A"] = base["Unnamed: 5"]

    jogos["Gols B"] = base["Unnamed: 7"]

    jogos["Seleção B"] = base["Unnamed: 9"]


    jogos = jogos.fillna("")


    print(
        "✅ Jogos:",
        len(jogos)
    )


    return jogos


# ============================================================
# PALPITES
# ============================================================

def preparar_palpites(df):

    print("🔄 Preparando palpites")


    lista = []


    colunas = list(df.columns)


    for inicio in range(
        0,
        len(colunas),
        10
    ):


        bloco = colunas[
            inicio:inicio+10
        ]


        if len(bloco) < 10:

            continue


        participante = (

            bloco[0]

            .replace(" Status","")

            .strip()

        )


        for indice, linha in df.head(104).iterrows():


            def inteiro(x):

                try:
                    return int(x)

                except:
                    return None



            lista.append(

                {

                    "Participantes":
                        participante,


                    "id_jogo":
                        indice+1,


                    "Palpite A":
                        inteiro(
                            linha[bloco[5]]
                        ),


                    "Palpite B":
                        inteiro(
                            linha[bloco[7]]
                        )

                }

            )


    resultado = pd.DataFrame(
        lista
    )


    print(
        "✅ Palpites:",
        len(resultado)
    )


    return resultado



# ============================================================
# PONTUAÇÃO REGULAMENTO 4.1
# ============================================================

def calcular_pontos(jogos, palpites):


    resultado = []


    for _, p in palpites.iterrows():


        pontos = 0


        jogo = jogos[

            jogos["id_jogo"]

            ==

            p["id_jogo"]

        ]


        if not jogo.empty:


            jogo = jogo.iloc[0]


            try:


                ga = int(jogo["Gols A"])

                gb = int(jogo["Gols B"])


                pa = p["Palpite A"]

                pb = p["Palpite B"]



                # 12 pontos - placar exato

                if ga == pa and gb == pb:


                    pontos = 12



                # 8 pontos - vencedor + um placar

                elif (

                    (
                        (ga-gb)*(pa-pb) > 0

                        or

                        (ga-gb == 0 and pa-pb == 0)
                    )

                    and

                    (
                        ga == pa

                        or

                        gb == pb
                    )

                ):


                    pontos = 8



                # 5 pontos - resultado correto

                elif (

                    (ga-gb)*(pa-pb) > 0

                    or

                    (ga-gb == 0 and pa-pb == 0)

                ):


                    pontos = 5



                # 2 pontos - um placar correto

                elif (

                    ga == pa

                    or

                    gb == pb

                ):


                    pontos = 2



            except:


                pontos = 0



        resultado.append(

            {

                "Participantes":
                    p["Participantes"],


                "Item 4.1. Fase de Grupo":
                    pontos

            }

        )


    return pd.DataFrame(
        resultado
    )



# ============================================================
# RANKING COM DESEMPATE OFICIAL
# ============================================================

def gerar_ranking(pontos):


    ranking = (

        pontos.groupby(

            "Participantes",

            as_index=False

        )

        .sum()

    )


    ranking["Acerto Campeão"] = 0

    ranking["Acerto Artilheiro"] = 0

    ranking["ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"] = 0

    ranking["ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º"] = 0


    ranking["Data Envio"] = range(
        1,
        len(ranking)+1
    )


    ranking["TOTAL"] = (

        ranking[
            "Item 4.1. Fase de Grupo"
        ]

        +

        ranking[
            "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"
        ]

        +

        ranking[
            "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º"
        ]

    )



    ranking = ranking.sort_values(

        [

            "TOTAL",

            "Acerto Campeão",

            "Acerto Artilheiro",

            "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias",

            "Data Envio"

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


    return ranking



# ============================================================
# MOTOR
# ============================================================

def executar_motor():

    print("="*80)

    print("🏆 MOTOR COPA 2026 v6.0")

    print("="*80)


    try:


        dados = carregar_dados()


        print(
            "✅ Google Sheets conectado"
        )


        jogos = preparar_jogos(
            dados["jogos"]
        )


        palpites = preparar_palpites(
            dados["palpites"]
        )


        pontos = calcular_pontos(
            jogos,
            palpites
        )


        ranking = gerar_ranking(
            pontos
        )


        if len(jogos) != 104:

            raise Exception(
                "Quantidade de jogos inválida"
            )


        if len(palpites) != 3120:

            raise Exception(
                "Quantidade de palpites inválida"
            )


        if len(ranking) != 30:

            raise Exception(
                "Quantidade de participantes inválida"
            )



        exportar_json(
            "ranking_geral.json",
            ranking
        )


        exportar_json(
            "jogos.json",
            jogos
        )


        exportar_json(
            "palpites.json",
            palpites
        )



        print()

        print(
            "🏆 MOTOR APROVADO PARA PRODUÇÃO"
        )


        return True



    except Exception as erro:


        print(
            "❌ ERRO MOTOR"
        )


        print(
            erro
        )


        traceback.print_exc()


        return False



if __name__ == "__main__":


    executar_motor()
