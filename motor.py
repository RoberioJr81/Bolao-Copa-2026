# ... (dentro da função rodar_motor, substitua o bloco abaixo)
        
        planilha = cliente.open_by_key(os.environ["SHEET_ID"])
        
        # Mapeamento para garantir que pegamos as abas certas
        # Dica: Verifique se na sua planilha não há espaços após o nome
        mapa_abas = {
            "participantes.json": "C_Participantes",
            "jogos.json": "C_Placares Oficiais",
            "palpites.json": "C_Palpites",
            "ranking_geral.json": "C_Ranking Geral"
        }
        
        for nome_arquivo, nome_aba in mapa_abas.items():
            try:
                # Tenta ler a aba pelo nome exato
                aba = planilha.worksheet(nome_aba)
                dados = aba.get_all_records()
                df = pd.DataFrame(dados)
                df = df.replace({pd.NA: None, float('nan'): None})
                salvar_json_seguro(nome_arquivo, df.to_dict("records"))
                logging.info(f"Sucesso: {nome_arquivo} carregado da aba {nome_aba}")
            except Exception as e:
                logging.error(f"Erro ao ler aba {nome_aba}: {e}")
