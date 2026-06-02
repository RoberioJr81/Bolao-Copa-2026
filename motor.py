# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v5.0
# ============================================================

import pandas as pd
import os
import traceback
from urllib.parse import quote


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

    df.to_json(
        os.path.join(PASTA_PUBLICACAO,nome),
        orient="records",
        force_ascii=False,
        indent=4
    )

    print("✅ JSON:", nome)



# ============================================================
# JOGOS
# ============================================================

def preparar_jogos(df):


    base = df[
        df["Partidas"].notna()
    ].reset_index(drop=True)


    jogos = pd.DataFrame()


    jogos["id_jogo"] = range(1,len(base)+1)


    jogos["Seleção A"] = base["Partidas"]


    jogos["Gols A"] = base["Unnamed: 5"]


    jogos["Gols B"] = base["Unnamed: 7"]


    jogos["Seleção B"] = base["Unnamed: 9"]


    return jogos.fillna("")



# ============================================================
# PALPITES — FORMATO HOMOLOGADO COLAB
# ============================================================

def preparar_palpites(df):


    print("📋 Colunas C_Palpites:")
    print(list(df.columns))


    mapa = {
        c.lower().strip(): c
        for c in df.columns
    }


    if (

        "participante" in mapa
        and "id_jogo" in mapa
        and "gols_a" in mapa
        and "gols_b" in mapa

    ):


        saida = pd.DataFrame()


        saida["Participante"] = df[
            mapa["participante"]
        ]


        saida["id_jogo"] = df[
            mapa["id_jogo"]
        ]


        saida["A"] = df[
            mapa["gols_a"]
        ]


        saida["B"] = df[
            mapa["gols_b"]
        ]


        print(
            "✅ Palpites formato Colab:",
            len(saida)
        )


        return saida



    raise Exception(
        "Formato C_Palpites não reconhecido"
    )



# ============================================================
# CÁLCULO ITEM 4.1
# ============================================================

def calcular_pontos(jogos,palpites):


    lista=[]


    for _,p in palpites.iterrows():


        jogo = jogos[
            jogos["id_jogo"] == p["id_jogo"]
        ]


        if jogo.empty:

            continue


        jogo=jogo.iloc[0]


        pontos=0


        try:

            ga=int(jogo["Gols A"])

            gb=int(jogo["Gols B"])


            if ga==p["A"] and gb==p["B"]:

                pontos=12


            elif (

                (ga-gb>0 and p["A"]-p["B"]>0)

                or

                (ga-gb<0 and p["A"]-p["B"]<0)

                or

                (ga-gb==0 and p["A"]-p["B"]==0)

            ):

                pontos=5


        except:

            pontos=0



        lista.append({

            "Participantes":
                p["Participante"],

            "Item 4.1. Fase de Grupo":
                pontos

        })


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


    ranking["ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"]=0

    ranking["ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º"]=0

    ranking["4.2. Artilheiro"]=0


    ranking["Total"] = (

        ranking["Item 4.1. Fase de Grupo"]

    )


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
# EXECUÇÃO
# ============================================================

def executar_motor():


    print("="*80)
    print("🏆 MOTOR COPA 2026 v5")
    print("="*80)


    try:


        dados=carregar_dados()


        jogos=preparar_jogos(
            dados["jogos"]
        )


        palpites=preparar_palpites(
            dados["palpites"]
        )


        pontos=calcular_pontos(
            jogos,
            palpites
        )


        ranking=gerar_ranking(
            pontos
        )


        print("🔒 AUDITOR")

        assert len(jogos)==104

        assert len(palpites)==3120

        assert len(ranking)==30


        print("✅ Jogos:",len(jogos))

        print("✅ Palpites:",len(palpites))

        print("✅ Ranking:",len(ranking))


        exportar_json(
            "ranking_geral.json",
            ranking
        )


        exportar_json(
            "jogos.json",
            jogos
        )


        print("🏆 MOTOR APROVADO")


        return True


    except Exception as erro:


        print("❌ ERRO MOTOR")

        print(erro)

        traceback.print_exc()

        return False



if __name__=="__main__":

    executar_motor()
