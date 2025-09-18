# models.py

import pandas as pd
import pyodbc

def get_transactions(start_date=None, end_date=None):
    conn_str = (
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=DMD;'
        'UID=sa;'
        'PWD=arte171721;'
        'Encrypt=yes;'
        'TrustServerCertificate=yes;'
    )

    try:
        connection = pyodbc.connect(conn_str)
        print("✅ Conexão com o banco de dados estabelecida")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        return pd.DataFrame({'erro': [f'Erro de conexão: {e}']})

    # Nomes das colunas e JOINS já validados
    col_codigo_nfsit = "Cod_Produto"
    col_chave_estabe_nfsit = "Cod_Estabe"
    col_codigo_produ = "Codigo"
    col_descricao_produ = "Descricao"
    col_data_nfscb = "Dat_Emissao"
    col_chave_estabe_nfscb = "Cod_Estabe"
    
    # ==============================================================================
    #       CORREÇÃO: Usando CAST para converter a string de data explicitamente
    # ==============================================================================
    
    # Consulta SQL com a conversão de data para evitar erros de formato
    consulta = f"""
    SELECT
        n.{col_codigo_nfsit},
        p.{col_descricao_produ} 
    FROM
        NFSIT AS n
    INNER JOIN
        PRODU AS p ON n.{col_codigo_nfsit} = p.{col_codigo_produ}
    INNER JOIN
        NFSCB AS c ON n.{col_chave_estabe_nfsit} = c.{col_chave_estabe_nfscb}
    WHERE
        c.{col_data_nfscb} >= CAST('{start_date}' AS DATE) AND c.{col_data_nfscb} <= CAST('{end_date}' AS DATE)
        AND n.{col_chave_estabe_nfsit} = 1 
        AND c.{col_chave_estabe_nfscb} = 1
    """

    print("Executando a consulta:", consulta)

    try:
        df = pd.read_sql(consulta, connection)
        print(f"📊 {len(df)} linhas retornadas do banco")
        
        if not df.empty and 'erro' not in df.columns:
            df.columns = ['codigo', 'descricao']

    except Exception as e:
        print("❌ Erro ao executar a consulta SQL:", e)
        df = pd.DataFrame({'erro': [f'Erro na consulta: {e}']})

    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("🔒 Conexão com o banco fechada")

    return df