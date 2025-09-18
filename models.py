# models.py

import pandas as pd
import pyodbc

# Função para obter transações do banco SQL Server
def get_transactions(start_date=None, end_date=None):
    # Configuração da conexão
    conn_str = (
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=localhost;'   # Ajuste conforme sua instância
        'DATABASE=DMD;'           # Substitua pelo nome do seu banco
        'UID=sa;'                          # Usuário correto
        'PWD=arte171721;'                    # Senha correta
        'Encrypt=yes;'                     # Mantém criptografia
        'TrustServerCertificate=yes;'      # Aceita certificado autoassinado
    )

    try:
        connection = pyodbc.connect(conn_str)
        print("✅ Conexão com o banco de dados estabelecida")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        # Retorna um DataFrame vazio com coluna de erro para exibir na tela
        return pd.DataFrame({'erro': [f'Erro de conexão: {e}']})

    # Consulta SQL corrigida conforme informado pelo usuário
    consulta = """
    SELECT NFSIT.Codigo, NFSIT.Descricao
    FROM NFSIT
    INNER JOIN PRODU ON NFSIT.Codigo = PRODU.Cod_Produto
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