# config.py

# Defina o ambiente ativo aqui: 'prod' ou 'teste'
ACTIVE_ENV = 'teste'

# Configurações de conexão para diferentes ambientes
DB_CONFIGS = {
    'prod': {
        "driver": "{ODBC Driver 18 for SQL Server}",
        "server": "localhost",
        "database": "DMD",
        "uid": "sa",
        "pwd": "arte171721",
        "encrypt": "yes",
        "trust_server_certificate": "yes"
    },
    'teste': {
        "driver": "{ODBC Driver 18 for SQL Server}",
        "server": "localhost",
        "database": "DMD_TESTE",
        "uid": "sa",
        "pwd": "arte171721",
        "encrypt": "yes",
        "trust_server_certificate": "yes"
    }
}
