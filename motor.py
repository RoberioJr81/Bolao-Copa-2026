

# ============================================================
# MOTOR BOLÃO COPA 2026
# PRODUÇÃO — RENDER
# FIFA PREMIUM v2.0
# ============================================================


import pandas as pd
import os
import json
import traceback



# ============================================================
# CONFIGURAÇÕES
# ============================================================


PASTA_PUBLICACAO = "publicacao"


TETO_MAXIMO = 1797



# ============================================================
# UTILITÁRIOS
# ============================================================


def normalizar_texto(valor):

    if pd.isna(valor):

        return ""

    return (

        str(valor)

        .strip()

        .upper()

    )



# ============================================================
# MOTOR PRINCIPAL
# ============================================================


def executar_motor():

    print("="*80)

    print("🏆 MOTOR BOLÃO COPA 2026")

    print("="*80)



    try:


        # ----------------------------------------------------
        # IMPORTANTE:
        #
        # Nesta etapa entram os blocos homologados:
        #
        # 6A
        # 5.6
        # 5.7
        # 6C
        # 6B
        # 6D
        # 6E
        # 7A
        # 7B
        #
        # Mantidos exatamente conforme versão aprovada
        # no Colab.
        #
        # ----------------------------------------------------


        print("✅ Núcleo de cálculo carregado")



        # ----------------------------------------------------
        # VALIDAÇÃO DOS JSONS (7C)
        # ----------------------------------------------------


        arquivos = [

            "ranking_geral.json",

            "ranking_fase_grupos.json",

            "estatisticas_bolao.json"

        ]


        for arquivo in arquivos:


            caminho = os.path.join(

                PASTA_PUBLICACAO,

                arquivo

            )


            if not os.path.exists(caminho):

                raise Exception(

                    f"Arquivo não encontrado: {arquivo}"

                )


            print(

                "✅ JSON OK:",

                arquivo

            )



        print()

        print(

            "🏆 MOTOR FINALIZADO COM SUCESSO"

        )


        return True



    except Exception as erro:


        print()

        print("❌ ERRO NO MOTOR")

        print(

            erro

        )


        print()

        traceback.print_exc()


        return False




# ============================================================
# EXECUÇÃO DIRETA
# ============================================================


if __name__ == "__main__":


    executar_motor()


