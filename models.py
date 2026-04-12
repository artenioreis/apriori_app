# models.py

import pandas as pd
import pyodbc
from config import ACTIVE_ENV, DB_CONFIGS

# Função para obter transações do banco SQL Server
def get_transactions(start_date, end_date): # As datas agora são obrigatórias
    # Configuração da conexão baseada no ambiente ativo
    config = DB_CONFIGS[ACTIVE_ENV]
    
    conn_str = (
        f"DRIVER={config['driver']};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['uid']};"
        f"PWD={config['pwd']};"
        f"Encrypt={config['encrypt']};"
        f"TrustServerCertificate={config['trust_server_certificate']};"
    )

    try:
        connection = pyodbc.connect(conn_str)
        print("✅ Conexão com o banco de dados estabelecida")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        # Retorna um DataFrame vazio com coluna de erro para exibir na tela
        return pd.DataFrame({'erro': [f'Erro de conexão: {e}']})

    # --- CORREÇÃO ---
    # Adicionamos "S.Num_Nota" à consulta. Este campo é crucial, pois
    # ele identifica unicamente cada transação de venda.
    consulta = """
    SELECT 
        S.Num_Nota,
        S.Cod_Produto,
        P.Descricao
    FROM 
        NFSIT AS S
    INNER JOIN 
        PRODU AS P ON S.Cod_Produto = P.Codigo
    INNER JOIN 
        NFSCB AS C ON S.Num_Nota = C.Num_Nota
    WHERE 
        CAST(C.Dat_Emissao AS DATE) BETWEEN ? AND ?;
    """

    try:
        # A execução da consulta continua a mesma, passando os parâmetros de forma segura.
        df = pd.read_sql(consulta, connection, params=(start_date, end_date))
        
        print(f"📊 {len(df)} linhas retornadas do banco para o período de {start_date} a {end_date}")

    except Exception as e:
        print("❌ Erro ao executar a consulta SQL:", e)
        df = pd.DataFrame({'erro': [f'Erro na consulta: {e}']})

    finally:
        connection.close()
        print("🔒 Conexão com o banco fechada")

    return df

