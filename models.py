import pyodbc
import pandas as pd
from config import DB_CONFIG

def get_connection():
    """Cria a conexão com o banco de dados SQL Server."""
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['uid']};"
        f"PWD={DB_CONFIG['pwd']}"
    )
    return pyodbc.connect(conn_str)

def get_transactions(start_date=None, end_date=None):
    """
    Busca os dados de vendas no banco de dados.
    - Se start_date e end_date forem fornecidos, filtra pelo intervalo de datas.
    """
    conn = get_connection()
    query = """
   SELECT Codigo, Descricao
FROM NFSIT
INNER JOIN PRODU
ON Codigo = Cod_Produto
    """
    if start_date:
        query += f" AND OrderDate >= '{start_date}'"
    if end_date:
        query += f" AND OrderDate <= '{end_date}'"

    df = pd.read_sql(query, conn)
    conn.close()
    return df

