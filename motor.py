# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v6.2
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

def exportar(nome, df):

    caminho = os.path.join(BASE_DIR, nome)

    df.to_json(
        caminho,
        orient="records",
        force_ascii=False,
        indent=4
    )

    print("✅ JSON criado:", nome)


# ============================================================
# FORMATAÇÃO SEGURA DE PLACAR
# ============================================================

def placar(a, b):

    try:

        if pd.isna(a) or pd.isna(b):
            return ""

        return f"{int(a)}x{int(b)}"

    except:

        return ""


# ============================================================
# PARTICIPANTES
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
        columns={coluna_nome:"Participantes"}
    )


    # NÃO ALTERA NOMES
    base["Participantes"] = (
        base["Participantes"]
        .astype(str)
        .str.strip()
    )


    if "ID" not in base.columns:

        base.insert(
            0,
            "ID",
            range(1, len(base)+1)
        )


    coluna_envio = None

    for c in base.columns:

        t = c.lower()

        if (
            "envio" in t
            or "receb" in t
            or "data" in t
        ):

            coluna_envio = c


    if coluna_envio:

        base["Data Envio"] = base[coluna_envio]

    else:

        base["Data Envio"] = ""


    base["Enviou"] = (
        base["Data Envio"]
        .astype(str)
        .str.len()
        > 3
    )


    return base[
        [
            "ID",
            "Participantes",
            "Data Envio",
            "Enviou"
        ]
    ]


# ============================================================
# JOGOS
# ============================================================

def preparar_jogos(df):

    jogos = pd.DataFrame()

    base = df.head(104).copy()


    jogos["Jogo"] = range(
        1,
        len(base)+1
    )


    jogos["Seleção A"] = base.iloc[:,3]

    jogos["Placar A"] = base.iloc[:,5]

    jogos["Placar B"] = base.iloc[:,7]

    jogos["Seleção B"] = base.iloc[:,9]


    jogos["Partida"] = (
        jogos["Seleção A"].astype(str)
        +
        " x "
        +
        jogos["Seleção B"].astype(str)
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

    registros=[]

    colunas=list(df.columns)


    for inicio in range(0,len(colunas),10):

        bloco=colunas[inicio:inicio+10]


        if len(bloco)<10:
            continue


        participante = (
            bloco[0]
            .replace(" Status","")
            .strip()
        )


        for i,linha in df.head(104).iterrows():

            registros.append(

                {

                    "Participantes":participante,

                    "Jogo":i+1,

                    "A":linha[bloco[5]],

                    "B":linha[bloco[7]]

                }

            )


    resultado=pd.DataFrame(registros)


    print(
        "✅ Palpites:",
        len(resultado)
    )


    return resultado


# ============================================================
# PONTUAÇÃO
# ============================================================

def calcular(jogos,palpites):

    resultado=[]


    for _,p in palpites.iterrows():

        pontos=0


        jogo=jogos[
            jogos["Jogo"]==p["Jogo"]
        ]


        if not jogo.empty:

            try:

                j=jogo.iloc[0]

                ga=int(j["Placar A"])
                gb=int(j["Placar B"])

                pa=int(p["A"])
                pb=int(p["B"])


                if ga==pa and gb==pb:

                    pontos=12


                elif (
                    ((ga-gb)*(pa-pb)>0)
                    or
                    (ga==gb and pa==pb)
                ):

                    if ga==pa or gb==pb:

                        pontos=8

                    else:

                        pontos=5


                elif ga==pa or gb==pb:

                    pontos=2


            except:

                pontos=0


        resultado.append(
            {
                "Participantes":p["Participantes"],
                "Fase de Grupo":pontos
            }
        )


    return pd.DataFrame(resultado)


# ============================================================
# MATRIZ PALPITES
# ============================================================

def matriz_palpites(jogos,palpites):

    linhas=[]


    oficial={"Nome":"Placar Oficial"}


    for _,j in jogos.iterrows():

        oficial[j["Partida"]] = placar(
            j["Placar A"],
            j["Placar B"]
        )


    linhas.append(oficial)


    for nome in palpites["Participantes"].unique():

        linha={"Nome":nome}


        dados=palpites[
            palpites["Participantes"]==nome
        ]


        for _,p in dados.iterrows():

            jogo=jogos[
                jogos["Jogo"]==p["Jogo"]
            ].iloc[0]


            linha[jogo["Partida"]] = placar(
                p["A"],
                p["B"]
            )


        linhas.append(linha)


    return pd.DataFrame(linhas)


# ============================================================
# RANKING
# ============================================================

def ranking(participantes,pontos):

    total = (

        pontos
        .groupby(
            "Participantes",
            as_index=False
        )
        .sum()

    )


    r = participantes.merge(
        total,
        how="left",
        on="Participantes"
    )


    r=r.fillna(0)


    r["Campeão"]=0
    r["Artilheiro"]=0
    r["Eliminatórias"]=0


    r["TOTAL"] = (

        r["Fase de Grupo"]

        +

        r["Eliminatórias"]

    )


    r=r.sort_values(

        [

            "TOTAL",
            "Campeão",
            "Artilheiro",
            "Eliminatórias",
            "Enviou",
            "Data Envio"

        ],

        ascending=[

            False,
            False,
            False,
            False,
            False,
            True

        ]

    )


    r.insert(
        0,
        "Ranking",
        range(1,len(r)+1)
    )


    return r


# ============================================================
# EXECUÇÃO
# ============================================================

def executar_motor():

    print("="*80)
    print("🏆 MOTOR COPA 2026 v6.2")
    print("="*80)


    try:

        dados=carregar_dados()


        participantes=preparar_participantes(
            dados["participantes"]
        )


        jogos=preparar_jogos(
            dados["jogos"]
        )


        palpites=preparar_palpites(
            dados["palpites"]
        )


        pontos=calcular(
            jogos,
            palpites
        )


        geral=ranking(
            participantes,
            pontos
        )


        matriz=matriz_palpites(
            jogos,
            palpites
        )


        exportar(
            "ranking_geral.json",
            geral
        )


        exportar(
            "ranking_fase_grupos.json",
            geral
        )


        exportar(
            "jogos.json",
            jogos
        )


        exportar(
            "palpites.json",
            palpites
        )


        exportar(
            "matriz_palpites.json",
            matriz
        )


        print(
            "🏆 MOTOR APROVADO PARA PRODUÇÃO"
        )


    except Exception as erro:

        print("❌ ERRO MOTOR")
        print(erro)
        traceback.print_exc()


if __name__=="__main__":

    executar_motor()
