# ==============================================================================
# 🏆 BOLÃO COPA DO MUNDO 2026
# MOTOR OFICIAL v8.2.2
#
# Google Sheets → Motor → JSON → APP
# ==============================================================================

import pandas as pd
import json
from urllib.parse import quote


# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

SHEET_ID = "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"
COTA = 200


# ==============================================================================
# GOOGLE SHEETS
# ==============================================================================

def carregar_aba(nome):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={quote(nome)}"
    )

    return pd.read_csv(url)


# ==============================================================================
# UTILIDADES
# ==============================================================================

def salvar_json(nome, dados):

    with open(nome, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4,
            default=str
        )

    print(f"✅ {nome} gerado")


def converter_data(valor):

    try:

        if pd.isna(valor):
            return pd.Timestamp.max

        valor = str(valor).strip()

        if valor == "":
            return pd.Timestamp.max

        return pd.to_datetime(
            valor,
            dayfirst=True
        )

    except:

        return pd.Timestamp.max


# ==============================================================================
# PONTUAÇÃO ITEM 4.1
# ==============================================================================

def calcular_pontos_jogo(real_a, real_b, palp_a, palp_b):

    try:
        real_a = int(real_a)
        real_b = int(real_b)
        palp_a = int(palp_a)
        palp_b = int(palp_b)

    except:
        return 0


    if real_a == palp_a and real_b == palp_b:
        return 12


    real = (
        "A" if real_a > real_b
        else "B" if real_b > real_a
        else "E"
    )


    palpite = (
        "A" if palp_a > palp_b
        else "B" if palp_b > palp_a
        else "E"
    )


    if real == palpite:

        if real_a == palp_a or real_b == palp_b:
            return 8

        return 5


    if real_a == palp_a or real_b == palp_b:
        return 2


    return 0


# ==============================================================================
# MOTOR
# ==============================================================================

def rodar_motor():

    print("🏆 Rodando Motor v8.2.2")


    # --------------------------------------------------------------------------
    # LEITURA
    # --------------------------------------------------------------------------

    participantes = carregar_aba(
        "C_Participantes"
    )

    jogos = carregar_aba(
        "C_Placares Oficiais"
    )

    palpites = carregar_aba(
        "C_Palpites"
    )


    participantes.columns = participantes.columns.str.strip()
    jogos.columns = jogos.columns.str.strip()
    palpites.columns = palpites.columns.str.strip()


    # --------------------------------------------------------------------------
    # JSONS BASE
    # --------------------------------------------------------------------------

    salvar_json(
        "participantes.json",
        participantes.to_dict(orient="records")
    )


    salvar_json(
        "jogos.json",
        jogos.to_dict(orient="records")
    )


    salvar_json(
        "palpites.json",
        palpites.to_dict(orient="records")
    )


    # --------------------------------------------------------------------------
    # RANKING
    # --------------------------------------------------------------------------

    lista = []


    for _, pessoa in participantes.iterrows():


        nome = str(
            pessoa.get(
                "Participantes",
                ""
            )
        ).strip()


        envio = converter_data(
            pessoa.get(
                "Data e hora do Palpite"
            )
        )


        # inscrito sem palpite não entra no ranking

        if envio == pd.Timestamp.max:
            continue


        pontos_grupo = 0
        pontos_eliminatorias = 0
        pontos_classificacao = 0
        pontos_artilheiro = 0


        total = (
            pontos_grupo
            +
            pontos_eliminatorias
            +
            pontos_classificacao
            +
            pontos_artilheiro
        )


        lista.append({

            "Participante":
                nome,

            "ITEM 4.1. Fase de Grupo":
                pontos_grupo,

            "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias":
                pontos_eliminatorias,

            "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º":
                pontos_classificacao,

            "4.2. Artilheiro":
                pontos_artilheiro,

            "TOTAL":
                total,

            "Acertou_Campeao":
                0,

            "Acertou_Artilheiro":
                0,

            "Pontos_Eliminatorias":
                pontos_eliminatorias,

            "_Envio":
                envio

        })


    ranking = pd.DataFrame(lista)


    ranking = ranking.sort_values(

        by=[

            "TOTAL",

            "Acertou_Campeao",

            "Acertou_Artilheiro",

            "Pontos_Eliminatorias",

            "_Envio"

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
        "posição",
        range(1, len(ranking)+1)
    )


    ranking_publico = ranking.drop(

        columns=[

            "Acertou_Campeao",

            "Acertou_Artilheiro",

            "Pontos_Eliminatorias",

            "_Envio"

        ]

    )


    salvar_json(
        "ranking_geral.json",
        ranking_publico.to_dict(orient="records")
    )


    salvar_json(
        "ranking_fase_grupos.json",
        ranking_publico[
            [
                "posição",
                "Participante",
                "ITEM 4.1. Fase de Grupo"
            ]
        ].to_dict(orient="records")
    )


    # --------------------------------------------------------------------------
    # PREMIAÇÃO
    # --------------------------------------------------------------------------

    total_arrecadado = (
        len(participantes)
        *
        COTA
    )


    salvar_json(

        "premiacao.json",

        {

            "Valores Arrecadados":

            {

                "Inscritos":
                    len(participantes),

                "Cota":
                    COTA,

                "Total":
                    total_arrecadado

            },


            "Podio Geral":

                ranking_publico.head(3)
                .to_dict(orient="records"),


            "Podio Fase Grupo":

                ranking_publico
                .sort_values(
                    by="ITEM 4.1. Fase de Grupo",
                    ascending=False
                )
                .head(3)
                .to_dict(orient="records")

        }

    )


    # --------------------------------------------------------------------------
    # ESTATÍSTICAS / AUDITORIA
    # --------------------------------------------------------------------------

    jogos_validos = jogos[

        jogos["Status"]
        .astype(str)
        .str.strip()
        .isin(
            [
                "Agendado",
                "Realizado",
                "Finalizado"
            ]
        )

    ]


    jogos_realizados = jogos_validos[

        jogos_validos["Status"]
        .astype(str)
        .str.strip()
        .isin(
            [
                "Realizado",
                "Finalizado"
            ]
        )

    ].shape[0]


    estatisticas = {

        "Inscritos":
            len(participantes),

        "Participantes":
            len(participantes),

        "Participantes_Ativos":
            len(ranking_publico),

        "Jogos":
            f"{jogos_realizados}/{len(jogos_validos)}",

        "Registros_Jogos":
            len(jogos),

        "Cota":
            COTA,

        "Arrecadado":
            total_arrecadado,

        "Lider":

            ranking_publico.iloc[0]["Participante"]

            if len(ranking_publico)

            else "-"

    }


    salvar_json(
        "estatisticas_bolao.json",
        estatisticas
    )


    salvar_json(

        "auditoria.json",

        {

            "Motor":
                "v8.2.2",

            "Status":
                "OK",

            "Inscritos":
                len(participantes),

            "Ranking":
                len(ranking_publico),

            "Jogos_Oficiais":
                len(jogos_validos),

            "Linhas_Carregadas":
                len(jogos)

        }

    )


    print("🏆 MOTOR v8.2.2 FINALIZADO")


# ==============================================================================
# EXECUÇÃO
# ==============================================================================

if __name__ == "__main__":

    rodar_motor()
