import pandas as pd
import json
import os
import gspread
from google.oauth2.service_account import Credentials


# ======================================================
# CONFIGURAÇÃO
# ======================================================

SHEET_ID = "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"

COTA = 200


# ======================================================
# GOOGLE
# ======================================================

def conectar_google():

    credenciais = json.loads(
        os.environ["GOOGLE_CREDENTIALS"]
    )

    creds = Credentials.from_service_account_info(
        credenciais,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    return gspread.authorize(creds).open_by_key(SHEET_ID)


# ======================================================
# UTILITÁRIOS
# ======================================================

def salvar_json(nome, dados):

    with open(nome, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=4,
            default=str
        )

    print(f"OK -> {nome}")


def numero(v):
    try:
        if pd.isna(v):
            return None
        return int(v)
    except:
        return None


def tratar_data(v):
    try:
        return pd.to_datetime(
            v,
            dayfirst=True
        )
    except:
        return pd.Timestamp.max


# ======================================================
# PONTUAÇÃO ITEM 4.1
# ======================================================

def calcular_pontos_jogo(real_a, real_b, pal_a, pal_b):

    ra = numero(real_a)
    rb = numero(real_b)
    pa = numero(pal_a)
    pb = numero(pal_b)

    if None in [ra, rb, pa, pb]:
        return 0


    # placar exato
    if ra == pa and rb == pb:
        return 12


    resultado_real = (
        "A" if ra > rb else
        "B" if rb > ra else
        "E"
    )

    resultado_palpite = (
        "A" if pa > pb else
        "B" if pb > pa else
        "E"
    )


    if resultado_real == resultado_palpite:

        if ra == pa or rb == pb:
            return 8

        return 5


    if ra == pa or rb == pb:
        return 2


    return 0


# ======================================================
# MOTOR PRINCIPAL
# ======================================================

def rodar_motor():

    sheet = conectar_google()


    participantes = pd.DataFrame(
        sheet.worksheet(
            "C_Participantes"
        ).get_all_records()
    )


    jogos_bruto = pd.DataFrame(
        sheet.worksheet(
            "C_Placares Oficiais"
        ).get_all_records()
    )


    palpites_bruto = pd.DataFrame(
        sheet.worksheet(
            "C_Palpites"
        ).get_all_records()
    )


    # ==================================================
    # PARTICIPANTES
    # ==================================================

    participantes["Efetivado"] = participantes[
        "Data e hora do Palpite"
    ].apply(
        lambda x:
        "Sim"
        if str(x).strip() != ""
        else "Não"
    )


    salvar_json(
        "participantes.json",
        participantes.to_dict(
            orient="records"
        )
    )


    efetivos = participantes[
        participantes["Efetivado"] == "Sim"
    ]


    # ==================================================
    # JOGOS TRATADOS
    # ==================================================

    jogos = []


    for idx, linha in jogos_bruto.iterrows():

        try:

            selecao_a = linha.get(
                "Partidas"
            )

            selecao_b = linha.get(
                "Unnamed: 9"
            )


            if (
                pd.isna(selecao_a)
                or pd.isna(selecao_b)
                or selecao_a == "Partidas"
            ):
                continue


            jogos.append({

                "Jogo":
                    len(jogos)+1,

                "Data":
                    linha.get(
                        "Primeira fase GRUPO A Dia"
                    ),

                "Sede":
                    linha.get(
                        "Sede"
                    ),

                "Seleção A":
                    selecao_a,

                "Placar":
                    f"{linha.get('Unnamed: 5','')}x{linha.get('Unnamed: 7','')}",

                "Seleção B":
                    selecao_b,

                "Status":
                    linha.get(
                        "Status"
                    )
            })


        except:
            pass



    salvar_json(
        "jogos.json",
        jogos
    )


    # ==================================================
    # RANKING
    # ==================================================

    ranking = []


    for _, pessoa in efetivos.iterrows():

        nome = pessoa[
            "Participantes"
        ]

        envio = tratar_data(
            pessoa[
                "Data e hora do Palpite"
            ]
        )


        ranking.append({

            "Participante": nome,

            "ITEM 4.1. Fase de Grupo": 0,

            "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias": 0,

            "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º": 0,

            "4.2. Artilheiro": 0,

            "TOTAL": 0,

            "Acertou_Campeao":0,

            "Acertou_Artilheiro":0,

            "Pontos_Eliminatorias":0,

            "_Envio": envio

        })


    ranking_df = pd.DataFrame(
        ranking
    )


    if not ranking_df.empty:

        ranking_df = ranking_df.sort_values(

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


        ranking_df.insert(
            0,
            "posição",
            range(
                1,
                len(ranking_df)+1
            )
        )


    ranking_exportar = ranking_df.drop(
        columns=[
            "_Envio",
            "Acertou_Campeao",
            "Acertou_Artilheiro",
            "Pontos_Eliminatorias"
        ],
        errors="ignore"
    )


    salvar_json(
        "ranking_geral.json",
        ranking_exportar.to_dict(
            orient="records"
        )
    )


    salvar_json(
        "ranking_fase_grupos.json",
        ranking_exportar.to_dict(
            orient="records"
        )
    )


    # ==================================================
    # PALPITES MATRIZ PREMIUM
    # ==================================================

    mapa = []


    oficial = {
        "Participante":
        "Placar Oficial"
    }


    for jogo in jogos:

        chave = (
            jogo["Seleção A"]
            +
            " x "
            +
            jogo["Seleção B"]
        )

        oficial[chave] = jogo["Placar"]


    mapa.append(oficial)



    for _, pessoa in efetivos.iterrows():

        linha = {

            "Participante":
            pessoa["Participantes"]

        }


        for jogo in jogos:

            chave = (
                jogo["Seleção A"]
                +
                " x "
                +
                jogo["Seleção B"]
            )

            linha[chave] = ""


        mapa.append(linha)


    salvar_json(
        "palpites.json",
        mapa
    )


    # ==================================================
    # PREMIAÇÃO
    # ==================================================

    total = (
        len(participantes)
        *
        COTA
    )


    podio = []


    for medalha, item in zip(
        ["🥇","🥈","🥉"],
        ranking_exportar.head(3).to_dict(
            orient="records"
        )
    ):

        podio.append({

            "Posição": medalha,

            "Participante":
                item["Participante"],

            "Pontos":
                item["TOTAL"],

            "Premiação":
                0

        })



    salvar_json(
        "premiacao.json",
        {

            "Participantes":
                len(participantes),

            "Cota":
                COTA,

            "Total":
                total,

            "Podio Geral":
                podio,

            "Podio Grupo":
                podio

        }
    )


    # ==================================================
    # ESTATÍSTICAS
    # ==================================================

    salvar_json(
        "estatisticas_bolao.json",
        {

            "Participantes":
                len(participantes),

            "Efetivados":
                len(efetivos),

            "Jogos":
                f"0/{len(jogos)}",

            "Arrecadado":
                total,

            "Lider":
                (
                    ranking_exportar.iloc[0]["Participante"]
                    if len(ranking_exportar)
                    else ""
                )

        }
    )


    salvar_json(
        "auditoria.json",
        {

            "Motor":"OK",

            "Participantes":
                len(participantes),

            "Efetivados":
                len(efetivos),

            "Jogos":
                len(jogos),

            "Ranking":
                len(ranking_exportar)

        }
    )


# ======================================================
# EXECUÇÃO
# ======================================================

if __name__ == "__main__":

    rodar_motor()
