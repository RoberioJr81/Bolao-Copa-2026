# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v6.1
# REGULAMENTO FINAL
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

    dados = {
        "participantes": carregar_aba("C_Participantes"),
        "jogos": carregar_aba("C_Placares Oficiais"),
        "palpites": carregar_aba("C_Palpites")
    }

    print("✅ Google Sheets conectado")

    return dados



# ============================================================
# EXPORTAR JSON
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
# PARTICIPANTES OFICIAIS
# ============================================================

def preparar_participantes(df):

    base = df.copy()

    coluna_nome = None

    for c in base.columns:

        if "particip" in c.lower() or "nome" in c.lower():

            coluna_nome = c


    if coluna_nome is None:

        coluna_nome = base.columns[1]


    base = base.rename(
        columns={
            coluna_nome:"Participantes"
        }
    )


    base["ID"] = range(
        1,
        len(base)+1
    )


    coluna_envio = None


    for c in base.columns:

        texto = c.lower()

        if (
            "envio" in texto
            or "data" in texto
            or "hora" in texto
        ):

            coluna_envio = c


    if coluna_envio:

        base["Data Envio"] = base[coluna_envio]

    else:

        base["Data Envio"] = "9999-12-31"


    return base[
        [
            "ID",
            "Participantes",
            "Data Envio"
        ]
    ]



# ============================================================
# JOGOS
# ============================================================

def preparar_jogos(df):

    base = df[

        df.iloc[:,0].notna()

        &

        df.iloc[:,2].notna()

    ].copy()


    jogos = pd.DataFrame()


    jogos["id_jogo"] = range(
        1,
        len(base)+1
    )


    jogos["Partida"] = (

        base["Partidas"].astype(str)

        +

        " x "

        +

        base["Unnamed: 9"].astype(str)

    )


    jogos["Seleção A"] = base["Partidas"]

    jogos["Seleção B"] = base["Unnamed: 9"]

    jogos["Gols A"] = base["Unnamed: 5"]

    jogos["Gols B"] = base["Unnamed: 7"]


    jogos = jogos.head(
        104
    )


    print(
        "✅ Jogos:",
        len(jogos)
    )


    return jogos.fillna("")



# ============================================================
# PALPITES
# ============================================================

def preparar_palpites(df):

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


        for i, linha in df.head(104).iterrows():


            def numero(v):

                try:

                    return int(v)

                except:

                    return None



            lista.append(

                {

                    "Participantes": participante,

                    "id_jogo": i+1,

                    "Palpite A": numero(
                        linha[bloco[5]]
                    ),

                    "Palpite B": numero(
                        linha[bloco[7]]
                    )

                }

            )


    resultado = pd.DataFrame(lista)


    print(
        "✅ Palpites:",
        len(resultado)
    )


    return resultado



# ============================================================
# PONTUAÇÃO 12 / 8 / 5 / 2 / 0
# ============================================================

def calcular_pontos(jogos,palpites):

    linhas=[]


    for _,p in palpites.iterrows():


        pontos=0


        jogo=jogos[
            jogos["id_jogo"]==p["id_jogo"]
        ]


        if not jogo.empty:


            try:

                jogo=jogo.iloc[0]


                ga=int(jogo["Gols A"])

                gb=int(jogo["Gols B"])

                pa=p["Palpite A"]

                pb=p["Palpite B"]



                if ga==pa and gb==pb:

                    pontos=12


                elif (
                    ((ga-gb)*(pa-pb)>0 or (ga==gb and pa==pb))
                    and
                    (ga==pa or gb==pb)
                ):

                    pontos=8


                elif (
                    (ga-gb)*(pa-pb)>0
                    or
                    (ga==gb and pa==pb)
                ):

                    pontos=5


                elif ga==pa or gb==pb:

                    pontos=2


            except:

                pontos=0



        linhas.append(

            {

                "Participantes":p["Participantes"],

                "Item 4.1. Fase de Grupo":pontos

            }

        )


    return pd.DataFrame(linhas)



# ============================================================
# MATRIZ PALPITES
# ============================================================

def gerar_matriz(jogos,palpites):

    matriz=[]


    linha={

        "Nome":"Partidas"

    }


    for _,j in jogos.iterrows():

        linha[j["Partida"]] = j["Partida"]


    matriz.append(linha)



    linha={

        "Nome":"Placar Oficial"

    }


    for _,j in jogos.iterrows():

        linha[j["Partida"]] = (
            str(j["Gols A"])
            +
            " x "
            +
            str(j["Gols B"])
        )


    matriz.append(linha)



    for nome in palpites["Participantes"].unique():


        linha={

            "Nome":nome

        }


        dados = palpites[
            palpites["Participantes"]==nome
        ]


        for _,p in dados.iterrows():


            jogo = jogos[
                jogos["id_jogo"]==p["id_jogo"]
            ].iloc[0]


            linha[jogo["Partida"]] = (

                str(p["Palpite A"])

                +

                " x "

                +

                str(p["Palpite B"])

            )


        matriz.append(linha)



    return pd.DataFrame(matriz)



# ============================================================
# RANKING
# ============================================================

def gerar_ranking(participantes,pontos):

    ranking = (

        participantes.merge(

            pontos.groupby(
                "Participantes",
                as_index=False
            ).sum(),

            on="Participantes",

            how="left"

        )

    )


    ranking = ranking.fillna(0)


    ranking["Acerto Campeão"]=0

    ranking["Acerto Artilheiro"]=0

    ranking["ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"]=0


    ranking["TOTAL"] = (

        ranking["Item 4.1. Fase de Grupo"]

        +

        ranking["ITEM 4.3. e 5 - Confrontos Fase Eliminatórias"]

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
        "Ranking",
        range(1,len(ranking)+1)
    )


    return ranking



# ============================================================
# MOTOR
# ============================================================

def executar_motor():

    print("="*80)

    print("🏆 MOTOR COPA 2026 v6.1")

    print("="*80)


    try:


        dados = carregar_dados()


        participantes = preparar_participantes(
            dados["participantes"]
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
            participantes,
            pontos
        )


        matriz = gerar_matriz(
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


        exportar_json(
            "palpites.json",
            palpites
        )


        exportar_json(
            "matriz_palpites.json",
            matriz
        )


        print(
            "🏆 MOTOR APROVADO PARA PRODUÇÃO"
        )


        return True



    except Exception as erro:


        print("❌ ERRO MOTOR")

        print(erro)

        traceback.print_exc()

        return False



if __name__=="__main__":

    executar_motor()
