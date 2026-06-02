import pandas as pd
import json
import os
import logging
import gspread

from google.oauth2.service_account import Credentials
from tenacity import retry, stop_after_attempt, wait_fixed


# ======================================================
# CONFIGURAÇÕES
# ======================================================

VERSAO = "Motor Oficial v9.0"

SHEET_ID = (
    os.environ.get(
        "SHEET_ID",
        "1cDAujojgWNg7SAoR8FQ9MReSB0FTgJvbdYGMjnDVt04"
    )
)

COTA = float(
    os.environ.get(
        "COTA",
        200
    )
)


# ======================================================
# LOGGING
# ======================================================

logging.basicConfig(

    filename="motor.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)


def log(msg):

    print(msg)

    logging.info(msg)



# ======================================================
# GOOGLE SHEETS
# ======================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(5)
)

def conectar_google():

    credenciais = json.loads(
        os.environ[
            "GOOGLE_CREDENTIALS"
        ]
    )


    creds = Credentials.from_service_account_info(

        credenciais,

        scopes=[

            "https://www.googleapis.com/auth/spreadsheets",

            "https://www.googleapis.com/auth/drive"

        ]

    )


    cliente = gspread.authorize(
        creds
    )


    return cliente.open_by_key(
        SHEET_ID
    )



# ======================================================
# UTILITÁRIOS
# ======================================================

def salvar_json(nome, dados):

    if dados is None:

        raise Exception(
            f"{nome} sem dados"
        )


    temp = nome + ".tmp"


    with open(

        temp,

        "w",

        encoding="utf-8"

    ) as arquivo:


        json.dump(

            dados,

            arquivo,

            ensure_ascii=False,

            indent=4,

            default=str

        )


    os.replace(
        temp,
        nome
    )


    log(
        f"✅ {nome} salvo"
    )



def numero(valor):

    try:

        if valor == "":

            return None

        return int(
            valor
        )

    except:

        return None



def converter_data(valor):

    try:

        return pd.to_datetime(

            valor,

            dayfirst=True

        )

    except:

        return pd.Timestamp.max



# ======================================================
# PONTUAÇÃO ITEM 4.1
# ======================================================

def calcular_pontos_jogo(
    real_a,
    real_b,
    palp_a,
    palp_b
):


    ra = numero(real_a)
    rb = numero(real_b)

    pa = numero(palp_a)
    pb = numero(palp_b)


    if None in [
        ra,
        rb,
        pa,
        pb
    ]:

        return 0



    if ra == pa and rb == pb:

        return 12



    resultado_real = (

        "A"
        if ra > rb

        else "B"
        if rb > ra

        else "E"

    )


    resultado_palpite = (

        "A"
        if pa > pb

        else "B"
        if pb > pa

        else "E"

    )



    if resultado_real == resultado_palpite:


        if (
            ra == pa
            or
            rb == pb
        ):

            return 8


        return 5



    if (
        ra == pa
        or
        rb == pb
    ):

        return 2


    return 0



# ======================================================
# MOTOR PRINCIPAL
# ======================================================

def rodar_motor():


    log(
        f"🏆 {VERSAO} iniciado"
    )



    # -----------------------------
    # LEITURA GOOGLE
    # -----------------------------

    sheet = conectar_google()


    participantes = pd.DataFrame(

        sheet.worksheet(

            "C_Participantes"

        ).get_all_records()

    )



    jogos = pd.DataFrame(

        sheet.worksheet(

            "C_Placares Oficiais"

        ).get_all_records()

    )



    palpites = pd.DataFrame(

        sheet.worksheet(

            "C_Palpites"

        ).get_all_records()

    )



    log(
        f"Participantes: {len(participantes)}"
    )


    log(
        f"Jogos brutos: {len(jogos)}"
    )



    # -----------------------------
    # PARTICIPANTES EFETIVOS
    # -----------------------------

    efetivos = participantes[

        participantes[

            "Data e hora do Palpite"

        ].astype(str).str.strip()

        != ""

    ].copy()



    # -----------------------------
    # RANKING
    # -----------------------------

    ranking = []


    for _, pessoa in efetivos.iterrows():


        nome = pessoa[

            "Participantes"

        ]


        pontos_grupo = 0


        # preparado para cálculo real
        # placares serão ativados
        # conforme jogos forem acontecendo


        ranking.append(

            {

                "Participante": nome,

                "ITEM 4.1. Fase de Grupo": pontos_grupo,

                "ITEM 4.3. e 5 - Confrontos Fase Eliminatórias": 0,

                "ITEM 4.2. Passagem de fase, Campeão, Vice, 3º e 4º": 0,

                "4.2. Artilheiro": 0,

                "Acertou_Campeao": 0,

                "Acertou_Artilheiro": 0,

                "Pontos_Eliminatorias": 0,

                "TOTAL": pontos_grupo,

                "_Envio": converter_data(

                    pessoa[
                        "Data e hora do Palpite"
                    ]

                )

            }

        )



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

            "_Envio"

        ],

        errors="ignore"

    )



    # -----------------------------
    # PREMIAÇÃO
    # -----------------------------

    total = (
        len(participantes)
        *
        COTA
    )


    premiacao = {


        "Valores Arrecadados": {

            "Participantes": int(
                len(participantes)
            ),

            "Cota": COTA,

            "Total": total

        },


        "Podio Geral":

            ranking_exportar.head(3)
            .to_dict(
                orient="records"
            ),


        "Podio Grupo":

            ranking_exportar.head(3)
            .to_dict(
                orient="records"
            )

    }



    # -----------------------------
    # ESTATÍSTICAS
    # -----------------------------


    estatisticas = {


        "Participantes":

            int(
                len(participantes)
            ),


        "Efetivados":

            int(
                len(efetivos)
            ),


        "Jogos":

            f"0/{len(jogos)}",


        "Arrecadado":

            float(
                total
            ),


        "Lider":

            ranking_exportar.iloc[0]["Participante"]

            if not ranking_exportar.empty

            else "-"

    }



    auditoria = {


        "Motor": VERSAO,

        "Status": "OK",

        "Participantes": int(len(participantes)),

        "Efetivados": int(len(efetivos)),

        "Jogos": int(len(jogos)),

        "Ranking": int(len(ranking_exportar))

    }



    # -----------------------------
    # EXPORTAÇÃO JSON
    # -----------------------------


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


    salvar_json(

        "participantes.json",

        participantes.to_dict(
            orient="records"
        )

    )


    salvar_json(

        "jogos.json",

        jogos.to_dict(
            orient="records"
        )

    )


    salvar_json(

        "palpites.json",

        palpites.to_dict(
            orient="records"
        )

    )


    salvar_json(

        "premiacao.json",

        premiacao

    )


    salvar_json(

        "estatisticas_bolao.json",

        estatisticas

    )


    salvar_json(

        "auditoria.json",

        auditoria

    )



    log(

        f"🏆 {VERSAO} finalizado com sucesso"

    )




if __name__ == "__main__":

    rodar_motor()
