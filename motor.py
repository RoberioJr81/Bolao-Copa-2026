# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v5.3
# ============================================================

import pandas as pd
import os
import traceback
from urllib.parse import quote


# ============================================================
# CONFIGURAÇÕES
# ============================================================

SHEET_ID = "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"

PASTA_PUBLICACAO = "publicacao"

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

        "participantes": carregar_aba("C_Participantes"),

        "jogos": carregar_aba("C_Placares Oficiais"),

        "palpites": carregar_aba("C_Palpites")

    }



# ============================================================
# EXPORTAÇÃO
# ============================================================

def exportar_json(nome, df):

    os.makedirs(
        PASTA_PUBLICACAO,
        exist_ok=True
    )

    df.to_json(

        os.path.join(
            PASTA_PUBLICACAO,
            nome
        ),

        orient="records",

        force_ascii=False,

        indent=4

    )

    print(
        "✅ JSON criado:",
        nome
    )



# ============================================================
# JOGOS OFICIAIS — VALIDADOR SEGURO
# ============================================================

def preparar_jogos(df):


    print(
        "🔄 Validando jogos oficiais"
    )


    base = df[

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



    jogos = jogos.fillna("")



    print(

        "✅ Jogos identificados:",

        len(jogos)

    )



    return jogos



# ============================================================
# PALPITES — CONVERSOR OFICIAL VALIDADO
# ============================================================

def preparar_palpites(df):


    print(
        "🔄 Convertendo C_Palpites"
    )


    lista = []


    colunas = list(
        df.columns
    )



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



        linhas = (

            df

            .reset_index(drop=True)

            .head(104)

        )



        for indice, linha in linhas.iterrows():



            try:


                gols_a = linha[
                    bloco[5]
                ]


            except:


                gols_a = 0



            try:


                gols_b = linha[
                    bloco[7]
                ]


            except:


                gols_b = 0



            try:

                gols_a = int(gols_a)

            except:

                gols_a = 0



            try:

                gols_b = int(gols_b)

            except:

                gols_b = 0




            lista.append(

                {

                    "Participante":
                        participante,

                    "id_jogo":
                        indice + 1,

                    "A":
                        gols_a,

                    "B":
                        gols_b

                }

            )



    resultado = pd.DataFrame(
        lista
    )



    print(

        "✅ Palpites convertidos:",

        len(resultado)

    )



    return resultado



# ============================================================
# ITEM 4.1 — PONTUAÇÃO
# ============================================================

def calcular_pontos(jogos, palpites):


    lista = []



    for _, p in palpites.iterrows():



        jogo = jogos[

            jogos["id_jogo"]

            ==

            p["id_jogo"]

        ]



        pontos = 0



        if not jogo.empty:



            jogo = jogo.iloc[0]



            try:


                ga = int(
                    jogo["Gols A"]
                )


                gb = int(
                    jogo["Gols B"]
                )



                if ga == p["A"] and gb == p["B"]:


                    pontos = 12



                elif (


                    (ga-gb > 0 and p["A"]-p["B"] > 0)

                    or

                    (ga-gb < 0 and p["A"]-p["B"] < 0)

                    or

                    (ga-gb == 0 and p["A"]-p["B"] == 0)


                ):


                    pontos = 5



            except:


                pontos = 0




        lista.append(

            {

                "Participantes":
                    p["Participante"],

                "Item 4.1. Fase de Grupo":
                    pontos

            }

        )



    return pd.DataFrame(lista)



# ============================================================
# RANKING
# ============================================================

def gerar_ranking(df):


    ranking = (

        df.groupby(

            "Participantes",

            as_index=False

        )

        .sum()

    )



    ranking["ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"] = 0

    ranking["ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º"] = 0

    ranking["4.2. Artilheiro"] = 0



    ranking["Total"] = ranking[

        "Item 4.1. Fase de Grupo"

    ]



    ranking = ranking.sort_values(

        "Total",

        ascending=False

    )



    ranking.insert(

        0,

        "Ranking",

        range(1,len(ranking)+1)

    )



    return ranking



# ============================================================
# EXECUTAR MOTOR
# ============================================================

def executar_motor():


    print("="*80)

    print("🏆 MOTOR COPA 2026 v5.3")

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



        print()

        print("🔒 AUDITOR PRODUÇÃO")



        if len(jogos) != 104:

            raise Exception(

                f"Jogos encontrados: {len(jogos)}"

            )



        if len(palpites) != 3120:

            raise Exception(

                f"Palpites encontrados: {len(palpites)}"

            )



        if len(ranking) != 30:

            raise Exception(

                f"Participantes encontrados: {len(ranking)}"

            )



        if ranking["Total"].max() > TETO_MAXIMO:

            raise Exception(

                "Teto máximo ultrapassado"

            )



        print("✅ Jogos:", len(jogos))

        print("✅ Palpites:", len(palpites))

        print("✅ Ranking:", len(ranking))



        exportar_json(

            "ranking_geral.json",

            ranking

        )



        exportar_json(

            "jogos.json",

            jogos

        )



        print()

        print(

            "🏆 MOTOR APROVADO PARA PRODUÇÃO"

        )



        return True



    except Exception as erro:



        print()

        print("❌ ERRO MOTOR")


        print(erro)



        traceback.print_exc()



        return False




if __name__ == "__main__":


    executar_motor()
