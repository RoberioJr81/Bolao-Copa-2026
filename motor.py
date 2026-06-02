import pandas as pd
import json
import os
import logging
import gspread

from datetime import datetime
from google.oauth2.service_account import Credentials
from tenacity import retry, stop_after_attempt, wait_fixed


# =====================================================
# CONFIGURAÇÃO
# =====================================================

VERSAO_MOTOR = "v9.0 ESTÁVEL"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =====================================================
# SALVAMENTO SEGURO JSON
# =====================================================

def salvar_json(nome, dados):
    """
    Salva JSON de forma atômica:
    primeiro grava .tmp, depois substitui.
    Evita JSON quebrado.
    """

    try:
        temp = nome + ".tmp"

        with open(temp, "w", encoding="utf-8") as f:
            json.dump(
                dados,
                f,
                ensure_ascii=False,
                indent=4
            )

        os.replace(temp, nome)

        logging.info(f"{nome} salvo")

    except Exception as erro:
        logging.error(f"Erro ao salvar {nome}: {erro}")

        raise erro


# =====================================================
# GOOGLE SHEETS
# =====================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(3)
)
def conectar_google():

    if "GOOGLE_CREDENTIALS" not in os.environ:
        raise Exception(
            "Variável GOOGLE_CREDENTIALS não encontrada no Render"
        )

    if "SHEET_ID" not in os.environ:
        raise Exception(
            "Variável SHEET_ID não encontrada no Render"
        )


    credenciais = json.loads(
        os.environ["GOOGLE_CREDENTIALS"]
    )


    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]


    creds = Credentials.from_service_account_info(
        credenciais,
        scopes=scopes
    )


    cliente = gspread.authorize(creds)


    return cliente.open_by_key(
        os.environ["SHEET_ID"]
    )


# =====================================================
# UTILITÁRIOS
# =====================================================

def limpar_dataframe(df):

    df = df.copy()

    df = df.where(
        pd.notnull(df),
        None
    )

    return df


def numero(valor):

    try:
        return float(valor)

    except:
        return 0


# =====================================================
# MOTOR PRINCIPAL
# =====================================================

def rodar_motor():

    logging.info(
        f"🏆 Motor {VERSAO_MOTOR} iniciado"
    )


    planilha = conectar_google()


    # =============================================
    # LEITURA DAS ABAS
    # =============================================

    participantes = pd.DataFrame(
        planilha
        .worksheet("C_Participantes")
        .get_all_records()
    )


    jogos = pd.DataFrame(
        planilha
        .worksheet("C_Placares Oficiais")
        .get_all_records()
    )


    palpites = pd.DataFrame(
        planilha
        .worksheet("C_Palpites")
        .get_all_records()
    )


    ranking = pd.DataFrame(
        planilha
        .worksheet("C_Ranking Geral")
        .get_all_records()
    )


    # =============================================
    # LIMPEZA
    # =============================================

    participantes = limpar_dataframe(
        participantes
    )

    jogos = limpar_dataframe(
        jogos
    )

    palpites = limpar_dataframe(
        palpites
    )

    ranking = limpar_dataframe(
        ranking
    )


    # =============================================
    # PARTICIPANTES EFETIVOS
    # =============================================

    if "Data e hora do Palpite" in participantes.columns:

        efetivos = participantes[

            participantes[
                "Data e hora do Palpite"
            ]
            .astype(str)
            .str.strip()
            .ne("")

        ]

    else:

        efetivos = pd.DataFrame()


    # =============================================
    # FINANCEIRO
    # =============================================

    cota = numero(
        os.getenv(
            "COTA",
            200
        )
    )


    total_arrecadado = (
        len(participantes)
        *
        cota
    )


    # =============================================
    # LÍDER
    # =============================================

    if (
        not ranking.empty
        and
        "Participante" in ranking.columns
    ):

        lider = str(
            ranking.iloc[0]["Participante"]
        )

    else:

        lider = "-"


    # =============================================
    # EXPORTAÇÃO PRINCIPAL
    # =============================================

    salvar_json(
        "participantes.json",
        participantes.to_dict("records")
    )


    salvar_json(
        "jogos.json",
        jogos.to_dict("records")
    )


    salvar_json(
        "palpites.json",
        palpites.to_dict("records")
    )


    salvar_json(
        "ranking_geral.json",
        ranking.to_dict("records")
    )


    # =============================================
    # PREMIAÇÃO
    # =============================================

    salvar_json(
        "premiacao.json",
        {

            "Valores Arrecadados": {

                "Participantes":
                    int(len(participantes)),

                "Efetivados":
                    int(len(efetivos)),

                "Cota":
                    cota,

                "Total":
                    total_arrecadado
            }
        }
    )


    # =============================================
    # ESTATÍSTICAS
    # SEMPRE DICIONÁRIO
    # =============================================

    salvar_json(
        "estatisticas_bolao.json",
        {

            "Participantes":
                int(len(participantes)),

            "Efetivados":
                int(len(efetivos)),

            "Jogos":
                int(len(jogos)),

            "Arrecadado":
                total_arrecadado,

            "Lider":
                lider,

            "Atualizado":
                datetime.now()
                .strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
        }
    )


    # =============================================
    # AUDITORIA
    # SEMPRE DICIONÁRIO
    # =============================================

    salvar_json(
        "auditoria.json",
        {

            "Motor":
                VERSAO_MOTOR,

            "Status":
                "OK",

            "Participantes":
                int(len(participantes)),

            "Efetivados":
                int(len(efetivos)),

            "Jogos":
                int(len(jogos)),

            "Ranking":
                int(len(ranking)),

            "Palpites":
                int(len(palpites)),

            "Última execução":
                datetime.now()
                .strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
        }
    )


    logging.info(
        f"✅ Motor {VERSAO_MOTOR} concluído"
    )


# =====================================================
# EXECUÇÃO MANUAL
# =====================================================

if __name__ == "__main__":

    rodar_motor()
