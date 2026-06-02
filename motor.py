# ============================================================
# 🏆 MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# MOTOR OFICIAL v6.3
# ============================================================

import pandas as pd
import json
import os

print("=" * 80)
print("🏆 MOTOR COPA 2026 v6.3")
print("=" * 80)


# ============================================================
# CONFIGURAÇÕES
# ============================================================

URL_PLANILHA = (
    "https://docs.google.com/spreadsheets/d/"
    "1Z7H8M7KvRZ3eREPLACE/export?format=xlsx"
)

ARQUIVOS = {
    "ranking": "ranking_geral.json",
    "jogos": "jogos.json",
    "palpites": "palpites.json",
    "matriz": "matriz_palpites.json"
}


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


def limpar(valor):
    """
    Preserva texto original.
    Apenas remove vazios técnicos.
    """
    if pd.isna(valor):
        return ""

    return str(valor).strip()


def numero(valor):
    try:
        if pd.isna(valor) or valor == "":
            return ""
        return int(float(valor))
    except:
        return ""


def placar(a, b):
    a = numero(a)
    b = numero(b)

    if a == "" or b == "":
        return ""

    return f"{a}x{b}"


# ============================================================
# CARREGAMENTO
# ============================================================

print("🔄 Carregando Google Sheets")

try:

    xls = pd.ExcelFile(URL_PLANILHA)

    participantes = pd.read_excel(
        xls,
        "C_Participantes"
    )

    jogos_raw = pd.read_excel(
        xls,
        "C_Placares Oficiais"
    )

    palpites_raw = pd.read_excel(
        xls,
        "C_Palpites"
    )

    print("✅ Google Sheets conectado")

except Exception as erro:
    print("❌ Erro Google Sheets")
    raise erro


# ============================================================
# PARTICIPANTES
# ============================================================

participantes = participantes.fillna("")

lista_participantes = []

for _, p in participantes.iterrows():

    nome = limpar(
        p.get("Participantes", "")
    )

    if nome == "":
        continue

    envio = limpar(
        p.get("Data Envio", "")
    )

    lista_participantes.append({

        "ID":
            limpar(
                p.get("ID", "")
            ),

        "Participantes":
            nome,

        "Data Envio":
            envio,

        "Enviou":
            True if envio != "" else False,

        "Fase de Grupo":
            0,

        "Campeão":
            0,

        "Artilheiro":
            0,

        "Eliminatórias":
            0,

        "TOTAL":
            0
    })


# ============================================================
# JOGOS
# ============================================================

jogos = []

for idx, j in jogos_raw.iterrows():

    selecao_a = limpar(
        j.get("Seleção A", "")
    )

    selecao_b = limpar(
        j.get("Seleção B", "")
    )

    if selecao_a == "" and selecao_b == "":
        continue

    jogos.append({

        "Jogo":
            idx + 1,

        "Data":
            limpar(
                j.get("Data", "")
            ),

        "Local":
            limpar(
                j.get("Local", "")
            ),

        "Seleção A":
            selecao_a,

        "Placar A":
            numero(
                j.get("Gols A", "")
            ),

        "Placar B":
            numero(
                j.get("Gols B", "")
            ),

        "Seleção B":
            selecao_b
    })


print(f"✅ Jogos: {len(jogos)}")


# ============================================================
# PALPITES
# ============================================================

palpites = []

matriz = []

cabecalho = ["Partidas"]

for j in jogos:

    cabecalho.append(
        f"{j['Seleção A']} x {j['Seleção B']}"
    )

matriz.append(cabecalho)


# --------------------
# LINHA PLACAR OFICIAL
# --------------------

linha_oficial = [
    "Placar Oficial"
]

for j in jogos:

    linha_oficial.append(
        placar(
            j["Placar A"],
            j["Placar B"]
        )
    )

matriz.append(
    linha_oficial
)


# --------------------
# PARTICIPANTES
# --------------------

for participante in lista_participantes:

    nome = participante["Participantes"]

    linha = [
        nome
    ]

    dados = palpites_raw[
        palpites_raw.astype(str)
        .apply(
            lambda x:
            x.str.contains(
                nome,
                regex=False
            )
        )
        .any(axis=1)
    ]

    for j in jogos:

        valor = ""

        if not dados.empty:

            linha_jogo = dados[
                dados.astype(str)
                .apply(
                    lambda x:
                    x.str.contains(
                        str(j["Jogo"]),
                        regex=False
                    )
                )
                .any(axis=1)
            ]

            if not linha_jogo.empty:

                r = linha_jogo.iloc[0]

                valor = placar(
                    r.get("Gols A", ""),
                    r.get("Gols B", "")
                )

        linha.append(valor)

        palpites.append({

            "Participante":
                nome,

            "Jogo":
                j["Jogo"],

            "Palpite":
                valor
        })

    matriz.append(linha)


print(
    f"✅ Palpites: {len(palpites)}"
)


# ============================================================
# RANKING OFICIAL
# ============================================================

ranking = pd.DataFrame(
    lista_participantes
)


# trava: quem enviou sempre acima

ranking["_envio_ordem"] = ranking["Enviou"].apply(
    lambda x: 0 if x else 1
)

ranking["_data_ordem"] = ranking["Data Envio"].replace(
    "",
    "999999999"
)


ranking = ranking.sort_values(

    by=[
        "TOTAL",
        "Campeão",
        "Artilheiro",
        "Eliminatórias",
        "_envio_ordem",
        "_data_ordem"
    ],

    ascending=[
        False,
        False,
        False,
        False,
        True,
        True
    ]

)


ranking.insert(
    0,
    "Ranking",
    range(
        1,
        len(ranking) + 1
    )
)


ranking = ranking.drop(
    columns=[
        "_envio_ordem",
        "_data_ordem"
    ]
)


# ============================================================
# EXPORTAÇÃO
# ============================================================

salvar_json(
    ARQUIVOS["ranking"],
    ranking.to_dict(
        orient="records"
    )
)

salvar_json(
    ARQUIVOS["jogos"],
    jogos
)

salvar_json(
    ARQUIVOS["palpites"],
    palpites
)

salvar_json(
    ARQUIVOS["matriz"],
    matriz
)


print("🏆 MOTOR APROVADO PARA PRODUÇÃO")
print("=" * 80)
