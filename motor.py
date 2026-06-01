# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v4.0
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

        "participantes":
            carregar_aba("C_Participantes"),

        "jogos":
            carregar_aba("C_Placares Oficiais"),

        "palpites":
            carregar_aba("C_Palpites")

    }



# ============================================================
# EXPORTAÇÃO
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
        "✅ Gerado:",
        nome
    )



# ============================================================
# PREPARAR JOGOS
# ============================================================

def preparar_jogos(df):


    base = df[

        df["Partidas"].notna()

    ].copy()


    base = base.reset_index(drop=True)


    jogos = pd.DataFrame()


    jogos["Jogo"] = range(
        1,
        len(base)+1
    )


    jogos["Fase"] = "Grupo"


    jogos["Seleção A"] = base["Partidas"]


    jogos["Gols A"] = base["Unnamed: 5"]


    jogos["Gols B"] = base["Unnamed: 7"]


    jogos["Seleção B"] = base["Unnamed: 9"]


    return jogos.fillna("")



# ============================================================
# PREPARAR PALPITES
# ============================================================

def preparar_palpites(df):


    lista = []


    for _, linha in df.iterrows():


        participante = linha["Participantes"]


        numero_jogo = 1


        for valor in linha.values:


            texto = (

                str(valor)

                .replace(" ","")

                .lower()

            )


            if "x" in texto:


                try:

                    a,b = texto.split("x")


                    lista.append(

                        {

                            "Participante":
                                participante,

                            "Jogo":
                                numero_jogo,

                            "A":
                                int(a),

                            "B":
                                int(b)

                        }

                    )


                    numero_jogo += 1


                except:

                    pass



    return pd.DataFrame(lista)



# ============================================================
# ITEM 4.1 / PLACARES
# ============================================================

def calcular_placares(jogos, palpites):


    resultado = []


    for _, p in palpites.iterrows():


        jogo = jogos[

            jogos["Jogo"] == p["Jogo"]

        ]


        if jogo.empty:

            continue


        jogo = jogo.iloc[0]


        pontos = 0


        try:


            oficial_a = int(jogo["Gols A"])

            oficial_b = int(jogo["Gols B"])



            if (

                oficial_a == p["A"]

                and

                oficial_b == p["B"]

            ):


                pontos = 12


            elif (

                (oficial_a-oficial_b > 0 and p["A"]-p["B"] > 0)

                or

                (oficial_a-oficial_b < 0 and p["A"]-p["B"] < 0)

                or

                (oficial_a-oficial_b == 0 and p["A"]-p["B"] == 0)

            ):


                pontos = 5


        except:


            pontos = 0



        resultado.append(

            {

                "Participante":
                    p["Participante"],

                "ITEM 4.1. Fase de Grupo":
                    pontos

            }

        )


    return pd.DataFrame(resultado)



# ============================================================
# RANKING
# ============================================================

def gerar_ranking(pontos, participantes):


    ranking = (

        pontos.groupby(

            "Participante",

            as_index=False

        )

        .sum()

    )


    ranking["ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"] = 0


    ranking["ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º"] = 0


    ranking["4.2. Artilheiro"] = 0


    ranking["TOTAL"] = (

        ranking["ITEM 4.1. Fase de Grupo"]

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
# AUDITOR
# ============================================================

def auditar(ranking, jogos, palpites):


    print()
    print("🔒 AUDITOR PRODUÇÃO")


    assert len(jogos) == 104, "Quantidade de jogos incorreta"


    assert len(palpites) == 3120, "Quantidade de palpites incorreta"


    assert ranking["TOTAL"].max() <= TETO_MAXIMO


    print("✅ Jogos: 104")
    print("✅ Palpites: 3120")
    print("✅ Teto respeitado")



# ============================================================
# EXECUTAR MOTOR
# ============================================================

def executar_motor():


    print("="*80)

    print("🏆 MOTOR BOLÃO COPA 2026")

    print("="*80)


    try:


        dados = carregar_dados()


        print("✅ Google Sheets conectado")


        jogos = preparar_jogos(

            dados["jogos"]

        )


        palpites = preparar_palpites(

            dados["palpites"]

        )


        pontos = calcular_placares(

            jogos,

            palpites

        )


        ranking = gerar_ranking(

            pontos,

            dados["participantes"]

        )


        auditar(

            ranking,

            jogos,

            palpites

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
        print("🏆 MOTOR APROVADO PARA PRODUÇÃO")


        return True



    except Exception as erro:


        print("❌ ERRO NO MOTOR")

        print(erro)


        traceback.print_exc()


        return False



if __name__ == "__main__":


    executar_motor()
