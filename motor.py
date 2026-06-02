# ============================================================
# 🏆 MOTOR COPA DO MUNDO 2026
# OFICIAL v6.4
# FIFA PREMIUM ENGINE
# ============================================================

import pandas as pd
import json
import os
import urllib.request
from io import BytesIO


print("=" * 80)
print("🏆 MOTOR COPA 2026 v6.4")
print("=" * 80)


# ============================================================
# CONFIGURAÇÃO GOOGLE SHEETS
# ============================================================

SHEET_ID = "COLOQUE_AQUI_SEU_ID_DO_GOOGLE_SHEETS"

URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=xlsx"
)


# ============================================================
# FUNÇÕES
# ============================================================

def salvar_json(nome, dados):

    with open(nome, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"✅ JSON criado: {nome}")



def achar_coluna(df, nomes):

    for c in df.columns:
        for n in nomes:
            if str(c).strip().lower() == n.lower():
                return c

    return None



def placar(a, b):

    if pd.isna(a) or pd.isna(b):
        return ""

    try:
        return f"{int(a)}x{int(b)}"

    except:
        return ""



# ============================================================
# CARREGAR GOOGLE SHEETS
# ============================================================

try:

    print("🔄 Carregando Google Sheets")

    arquivo = urllib.request.urlopen(
        URL,
        timeout=20
    ).read()

    xls = pd.ExcelFile(BytesIO(arquivo))

    print("✅ Google Sheets conectado")


except Exception as e:

    print("❌ Erro Google Sheets")
    print(e)

    print("⚠️ Mantendo JSON existente")
    exit()



# ============================================================
# PARTICIPANTES
# ============================================================

participantes = pd.read_excel(
    xls,
    "C_Participantes"
)


COL_ID = achar_coluna(
    participantes,
    ["ID", "Id"]
)

COL_NOME = achar_coluna(
    participantes,
    [
        "Participantes",
        "Participante",
        "Nome"
    ]
)

COL_ENVIO = achar_coluna(
    participantes,
    [
        "Data Envio",
        "Envio",
        "Data"
    ]
)


participantes = participantes.fillna("")


# TRAVA DE NOMES
participantes["NOME_OFICIAL"] = (
    participantes[COL_NOME]
    .astype(str)
)



# ============================================================
# JOGOS
# ============================================================

placares = pd.read_excel(
    xls,
    "C_Placares Oficiais"
)


COL_JOGO = achar_coluna(
    placares,
    ["Jogo", "ID_Jogo", "id_jogo"]
)

COL_DATA = achar_coluna(
    placares,
    ["Data"]
)

COL_SEDE = achar_coluna(
    placares,
    ["Sede", "Local"]
)

COL_A = achar_coluna(
    placares,
    ["Seleção A", "Time A"]
)

COL_B = achar_coluna(
    placares,
    ["Seleção B", "Time B"]
)

COL_GA = achar_coluna(
    placares,
    ["Gols A", "Placar A"]
)

COL_GB = achar_coluna(
    placares,
    ["Gols B", "Placar B"]
)


jogos = []

for _, j in placares.iterrows():

    jogos.append({

        "Jogo":
            j.get(COL_JOGO, ""),

        "Data":
            str(j.get(COL_DATA, "")),

        "Sede":
            j.get(COL_SEDE, ""),

        "Seleção A":
            j.get(COL_A, ""),

        "Placar A":
            "" if COL_GA is None else j.get(COL_GA, ""),

        "Placar B":
            "" if COL_GB is None else j.get(COL_GB, ""),

        "Seleção B":
            j.get(COL_B, "")

    })


print(f"✅ Jogos: {len(jogos)}")



# ============================================================
# PALPITES
# ============================================================

palpites = pd.read_excel(
    xls,
    "C_Palpites"
)

palpites = palpites.fillna("")


lista_palpites = (
    palpites
    .to_dict("records")
)


print(
    f"✅ Palpites: {len(lista_palpites)}"
)



# ============================================================
# RANKING
# ============================================================

ranking = []


for _, p in participantes.iterrows():


    nome = p["NOME_OFICIAL"]


    enviado = (
        str(
            p.get(COL_ENVIO, "")
        ).strip()
        != ""
    )


    fase_grupo = 0
    eliminatorias = 0
    item42 = 0
    campeao = 0
    artilheiro = 0


    total = (
        fase_grupo
        + eliminatorias
        + item42
        + campeao
        + artilheiro
    )


    ranking.append({

        "Participantes":
            nome,

        "ITEM 4.1. Fase de Grupo":
            fase_grupo,

        "ITEM 4.3 e 5 - Confrontos Fase Eliminatórias":
            eliminatorias,

        "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º":
            item42,

        "4.2. Artilheiro":
            artilheiro,

        "Total":
            total,


        # CAMPOS INTERNOS
        "_campeao":
            campeao,

        "_artilheiro":
            artilheiro,

        "_envio":
            p.get(COL_ENVIO, ""),

        "_enviado":
            enviado

    })



ranking = pd.DataFrame(ranking)


ranking = ranking.sort_values(

    by=[
        "Total",
        "_campeao",
        "_artilheiro",
        "ITEM 4.3 e 5 - Confrontos Fase Eliminatórias",
        "_enviado",
        "_envio"
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


ranking.insert(
    0,
    "Posição",
    range(
        1,
        len(ranking)+1
    )
)


ranking_json = (
    ranking
    .to_dict("records")
)



# ============================================================
# MATRIZ DE PALPITES
# ============================================================

matriz = []


linha_partidas = {
    "Participantes":
    "Partidas"
}


linha_oficial = {
    "Participantes":
    "Placar Oficial"
}



for _, j in placares.iterrows():

    chave = (
        str(j.get(COL_A,""))
        +
        " x "
        +
        str(j.get(COL_B,""))
    )

    linha_partidas[chave] = chave

    linha_oficial[chave] = placar(
        j.get(COL_GA,""),
        j.get(COL_GB,"")
    )



matriz.append(
    linha_partidas
)

matriz.append(
    linha_oficial
)



for _, p in participantes.iterrows():

    linha = {
        "Participantes":
        p["NOME_OFICIAL"]
    }


    for c in linha_partidas:

        if c != "Participantes":
            linha[c] = ""


    matriz.append(linha)



# ============================================================
# EXPORTAÇÃO
# ============================================================


salvar_json(
    "ranking_geral.json",
    ranking_json
)

salvar_json(
    "jogos.json",
    jogos
)

salvar_json(
    "palpites.json",
    lista_palpites
)

salvar_json(
    "matriz_palpites.json",
    matriz
)


print("🏆 MOTOR APROVADO PARA PRODUÇÃO")
print("=" * 80)
