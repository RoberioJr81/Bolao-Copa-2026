# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v4.1
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


    base = base.reset_index(
        drop=True
    )


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


    print(
        "📋 Colunas palpites:",
        list(df.columns)
    )


    for _, linha in df.iterrows():


        if "Participantes" in df.columns:

            participante = linha["Participantes"]


        elif "participante" in df.columns:

            participante = linha["participante"]


        else:

            participante = linha.iloc[0]



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
# ITEM 4.1
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


            oa = int(jogo["Gols A"])

            ob = int(jogo["Gols B"])



            if oa == p["A"] and ob == p["B"]:

                pontos = 12


            elif (

                (oa-ob > 0 and p["A"]-p["B"] > 0)

                or

                (oa-ob < 0 and p["A"]-p["B"] < 0)

                or

                (oa-ob == 0 and p["A"]-p["B"] == 0)

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

def gerar_ranking(pontos):


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


    ranking["TOTAL"] = ranking[
        "ITEM 4.1. Fase de Grupo"
    ]


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


    assert len(jogos) == 104


    assert len(palpites) == 3120


    assert ranking["TOTAL"].max() <= TETO_MAXIMO


    print("✅ Jogos:", len(jogos))

    print("✅ Palpites:", len(palpites))

    print("✅ Ranking:", len(ranking))

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
            pontos
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
