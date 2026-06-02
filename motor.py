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
# GOOGLE SHEETS
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

    print(f"✅ {nome} salvo")


def tratar_data(valor):

    try:
        if str(valor).strip() == "":
            return pd.Timestamp.max

        return pd.to_datetime(
            valor,
            dayfirst=True
        )

    except:

        return pd.Timestamp.max



# ======================================================
# MOTOR
# ======================================================

def rodar_motor():

    print("🏆 Motor v8.3.2 iniciado")


    # --------------------------------------------------
    # LEITURA GOOGLE
    # --------------------------------------------------

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
        if str(x).strip()
        else "Não"
    )


    efetivos = participantes[
        participantes["Efetivado"] == "Sim"
    ]


    salvar_json(
        "participantes.json",
        participantes.to_dict(
            orient="records"
        )
    )



    # ==================================================
    # JOGOS
    # ==================================================

    jogos = []


    for _, linha in jogos_bruto.iterrows():

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
                or str(selecao_a).strip() == ""
            ):
                continue


            jogos.append(

                {

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

                }

            )


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


        ranking.append(

            {

                "Participante":
                    pessoa["Participantes"],


                "ITEM 4.1. Fase de Grupo":
                    0,


                "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias":
                    0,


                "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º":
                    0,


                "4.2. Artilheiro":
                    0,


                "TOTAL":
                    0,


                "Acertou_Campeao":
                    0,


                "Acertou_Artilheiro":
                    0,


                "Pontos_Eliminatorias":
                    0,


                "_Envio":
                    tratar_data(
                        pessoa[
                            "Data e hora do Palpite"
                        ]
                    )

            }

        )


    ranking = pd.DataFrame(ranking)


    if not ranking.empty:

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
            range(
                1,
                len(ranking)+1
            )
        )



    ranking_exportar = ranking.drop(

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
    # PALPITES
    # ==================================================

    mapa = []


    oficial = {

        "Participante":
            "Placar Oficial"

    }


    for jogo in jogos:

        oficial[
            jogo["Seleção A"]
            +
            " x "
            +
            jogo["Seleção B"]
        ] = jogo["Placar"]


    mapa.append(oficial)


    for _, pessoa in efetivos.iterrows():

        linha = {

            "Participante":
                pessoa["Participantes"]

        }


        for jogo in jogos:

            linha[
                jogo["Seleção A"]
                +
                " x "
                +
                jogo["Seleção B"]
            ] = ""


        mapa.append(linha)



    salvar_json(
        "palpites.json",
        mapa
    )



    # ==================================================
    # PREMIAÇÃO
    # ==================================================

    total = len(participantes) * COTA


    podio = []


    for medalha, item in zip(

        ["🥇","🥈","🥉"],

        ranking_exportar.head(3)
        .to_dict(
            orient="records"
        )

    ):

        podio.append(

            {

                "Posição":
                    medalha,

                "Participante":
                    item["Participante"],

                "Pontuação":
                    item["TOTAL"],

                "Premiação":
                    0

            }

        )



    salvar_json(

        "premiacao.json",

        {

            "Valores Arrecadados":

            {

                "Participantes":
                    int(len(participantes)),

                "Cota":
                    float(COTA),

                "Total":
                    float(total)

            },


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
                int(len(participantes)),

            "Efetivados":
                int(len(efetivos)),

            "Jogos":
                f"0/{len(jogos)}",

            "Arrecadado":
                float(total),

            "Lider":
                str(
                    ranking_exportar.iloc[0]
                    ["Participante"]
                )
                if not ranking_exportar.empty
                else "-"

        }

    )



    # ==================================================
    # AUDITORIA
    # ==================================================

    salvar_json(

        "auditoria.json",

        {

            "Motor":
                "v8.3.2",

            "Status":
                "OK",

            "Participantes":
                int(len(participantes)),

            "Efetivados":
                int(len(efetivos)),

            "Jogos":
                int(len(jogos)),

            "Ranking":
                int(len(ranking_exportar)),

            "Palpites":
                "OK",

            "Premiacao":
                "OK"

        }

    )


    print("🏆 Motor v8.3.2 finalizado")



# ======================================================
# EXECUÇÃO
# ======================================================

if __name__ == "__main__":

    rodar_motor()
