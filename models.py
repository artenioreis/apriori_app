# models.py

import pandas as pd
import pyodbc

# Função para obter transações do banco SQL Server
def get_transactions(start_date=None, end_date=None):
    # Configuração da conexão
    conn_str = (
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=ARTENIOREIS;'   # Substitua pelo nome ou IP do seu servidor
        'DATABASE=DMD;'   # Substitua pelo nome do seu banco
        'UID=sa;'       # Substitua pelo usuário
        'PWD=arte171721;' # Substitua pela senha
    )

    try:
        connection = pyodbc.connect(conn_str)
        print("✅ Conexão com o banco de dados estabelecida")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        # Retorna um DataFrame vazio com coluna de erro para exibir na tela
        return pd.DataFrame({'erro': [f'Erro de conexão: {e}']})

    # Defina a coluna de data correta do seu banco (ex: DataPedido, DataEmissao, etc.)
    data_col = 'DataPedido'

    # Consulta SQL com filtro de data no WHERE
    consulta = f"""
    SELECT NFSIT.Codigo, NFSIT.Descricao
    FROM NFSIT
    INNER JOIN PRODU ON NFSIT.Codigo = PRODU.Cod_Produto
    WHERE NFSIT.{data_col} >= '{start_date}' AND NFSIT.{data_col} <= '{end_date}'
    """

    try:
        df = pd.read_sql(consulta, connection)
        print(f"📊 {len(df)} linhas retornadas do banco")
    except Exception as e:
        print("❌ Erro ao executar a consulta SQL:", e)
        df = pd.DataFrame({'erro': [f'Erro na consulta: {e}']})

    finally:
        connection.close()
        print("🔒 Conexão com o banco fechada")

    return df