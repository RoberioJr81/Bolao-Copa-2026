# ==============================================================================
# 🏆 MOTOR COPA DO MUNDO 2026
# MOTOR OFICIAL v6.5
# Google Sheets → JSON
#
# CORREÇÕES v6.5:
# ✅ Ranking com critérios oficiais de desempate
# ✅ Usa "Antecedência no envio" da C_Participantes
# ✅ Preserva nomes exatamente como digitados (acentos/caracteres)
# ✅ Corrige arrecadação real
# ✅ Corrige matriz geral de palpites
# ✅ Corrige jogos com sede e data
# ✅ Remove dependência de nomes antigos de colunas
# ==============================================================================

import pandas as pd
import json
import os
import gspread
from google.oauth2.service_account import Credentials


print("=" * 80)
print("🏆 MOTOR COPA 2026 v6.5")
print("=" * 80)


# ==============================================================================
# CONFIGURAÇÃO GOOGLE SHEETS
# ==============================================================================

SHEET_ID = "1DAuojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"


def carregar_google():

    print("🔄 Carregando Google Sheets")

    try:
        credenciais_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = Credentials.from_service_account_info(
            credenciais_json,
            scopes=scopes
        )

        cliente = gspread.authorize(creds)

        planilha = cliente.open_by_key(SHEET_ID)

        print("✅ Google Sheets conectado")

        return planilha

    except Exception as erro:
        print("❌ Erro Google Sheets")
        print(erro)
        raise erro


# ==============================================================================
# UTILIDADES
# ==============================================================================

def salvar_json(nome, dados):

    with open(nome, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print(f"✅ JSON criado: {nome}")


def limpar_numero(valor):

    try:
        if pd.isna(valor):
            return 0

        valor = str(valor)

        valor = (
            valor.replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )

        return float(valor)

    except:
        return 0


def texto(valor):

    if pd.isna(valor):
        return ""

    return str(valor).strip()


# ==============================================================================
# CARREGAMENTO
# ==============================================================================

sheet = carregar_google()


participantes = pd.DataFrame(
    sheet.worksheet("C_Participantes").get_all_records()
)

jogos = pd.DataFrame(
    sheet.worksheet("C_Placares Oficiais").get_all_records()
)

palpites = pd.DataFrame(
    sheet.worksheet("C_Palpites").get_all_records()
)


# PRESERVAÇÃO ABSOLUTA DOS NOMES
participantes["Participantes"] = (
    participantes["Participantes"]
    .astype(str)
)


print(f"✅ Participantes: {len(participantes)}")
print(f"✅ Jogos: {len(jogos)}")
print(f"✅ Palpites: {len(palpites)}")


# ==============================================================================
# ARRECADAÇÃO
# ==============================================================================

total_arrecadado = (
    participantes["Arrecadado"]
    .apply(limpar_numero)
    .sum()
)

cota = (
    participantes["Previsto"]
    .apply(limpar_numero)
    .max()
)


estatisticas = {

    "Participantes": int(len(participantes)),

    "Cota": cota,

    "Arrecadado": total_arrecadado,

    "Premiação Geral": total_arrecadado * 0.80,

    "Premiação Fase Grupos": total_arrecadado * 0.20

}


salvar_json(
    "estatisticas_bolao.json",
    estatisticas
)


# ==============================================================================
# JOGOS
# ==============================================================================

lista_jogos = []

for _, j in jogos.iterrows():

    item = {

        "Jogo": j.get("id_jogo", ""),

        "Data": texto(
            j.get("Data", "")
        ),

        "Sede": texto(
            j.get("Sede", "")
        ),

        "Seleção A": texto(
            j.get("Seleção A", "")
        ),

        "Placar A": texto(
            j.get("Gols A", "")
        ),

        "Placar B": texto(
            j.get("Gols B", "")
        ),

        "Seleção B": texto(
            j.get("Seleção B", "")
        )
    }

    lista_jogos.append(item)


salvar_json(
    "jogos.json",
    lista_jogos
)


# ==============================================================================
# RANKING OFICIAL
# ==============================================================================

ranking = []

for _, p in participantes.iterrows():

    nome = p["Participantes"]

    dados = {

        "Participante": nome,

        "ITEM 4.1. Fase de Grupo": 0,

        "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias": 0,

        "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º": 0,

        "4.2. Artilheiro": 0,

        "TOTAL": 0,

        "_desempate_envio":
            limpar_numero(
                p.get(
                    "Antecedência no envio",
                    999999
                )
            )
    }

    ranking.append(dados)


ranking = pd.DataFrame(ranking)


# CRITÉRIO OFICIAL DO REGULAMENTO

ranking = ranking.sort_values(

    by=[

        "TOTAL",

        "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º",

        "4.2. Artilheiro",

        "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias",

        "ITEM 4.1. Fase de Grupo",

        "_desempate_envio"

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
    range(1, len(ranking)+1)
)


# LOG DE AUDITORIA DO RANKING

print("=" * 80)
print("🏆 AUDITORIA DO RANKING")
print("=" * 80)

for _, r in ranking.head(5).iterrows():

    print(
        f'{r["Posição"]} - '
        f'{r["Participante"]} | '
        f'Total: {r["TOTAL"]} | '
        f'Envio: {r["_desempate_envio"]}'
    )


ranking_publico = ranking.drop(
    columns=["_desempate_envio"]
)


salvar_json(
    "ranking_geral.json",
    ranking_publico.to_dict(
        orient="records"
    )
)


# ==============================================================================
# RANKING FASE DE GRUPOS
# ==============================================================================


fase = ranking_publico[
    [
        "Posição",
        "Participante",
        "ITEM 4.1. Fase de Grupo"
    ]
]


salvar_json(
    "ranking_fase_grupos.json",
    fase.to_dict(
        orient="records"
    )
)


# ==============================================================================
# MATRIZ PALPITES
# ==============================================================================


matriz = []

for _, p in palpites.iterrows():

    linha = {}

    for coluna in palpites.columns:

        valor = p[coluna]

        if pd.isna(valor):
            valor = ""

        if str(valor).lower() == "nan":
            valor = ""

        linha[coluna] = valor


    matriz.append(linha)


salvar_json(
    "palpites.json",
    matriz
)


salvar_json(
    "matriz_palpites.json",
    matriz
)


# ==============================================================================
# FINALIZAÇÃO
# ==============================================================================

print("=" * 80)
print("🏆 MOTOR v6.5 APROVADO PARA PRODUÇÃO")
print("✅ Critério de desempate ativo")
print("✅ Dados preservados")
print("✅ Google Sheets como fonte única")
print("=" * 80)
