# Apriori App - Análise de Regras de Associação

## Descrição

Este projeto é um sistema web desenvolvido em Python com Flask para análise de dados de vendas utilizando o algoritmo Apriori. Ele permite identificar produtos mais vendidos, gerar regras de associação, sugerir kits de produtos e visualizar gráficos interativos.

O sistema conecta-se a um banco de dados SQL Server e processa as transações para gerar insights sobre padrões de compra.

---

## Funcionalidades

* Conexão com banco de dados SQL Server.
* Preparação de dados com padronização de colunas e conversão para formato binário para Apriori.
* Execução do algoritmo Apriori com suporte mínimo ajustável.
* Geração de regras de associação filtradas por confiança mínima.
* Visualização de gráficos interativos:

  * Top produtos mais vendidos
  * Relação confiança x lift
* Sugestão de kits de produtos com base nas regras geradas.
* Interface web responsiva com CSS personalizado.

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu_usuario/apriori_app.git
cd apriori_app
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux / macOS
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure a conexão com o banco de dados SQL Server no arquivo `models.py`.

---

## Como Executar

1. Ative o ambiente virtual (se ainda não estiver ativo).
2. Rode o aplicativo Flask:

```bash
python app.py
```

3. Acesse no navegador:

```
http://127.0.0.1:5000/
```

4. Utilize o formulário para filtrar por datas, suporte mínimo e confiança mínima.

---

## Estrutura do Projeto

```
apriori_app/
│
├── app.py                # Aplicativo Flask
├── services.py           # Funções de preparação de dados e Apriori
├── models.py             # Conexão e consulta ao banco de dados SQL Server
├── templates/
│   └── index.html        # Interface HTML
├── static/
│   └── style.css         # Estilos CSS
├── requirements.txt      # Dependências Python
└── README.md             # Este arquivo
```

---

## Dependências

* Flask
* pandas
* mlxtend
* plotly
* pyodbc (para SQL Server)

Instale todas com:

```bash
pip install -r requirements.txt
```

---

## Observações

* Certifique-se de que o DataFrame de entrada tenha colunas `codigo` e/ou `descricao`. Se `codigo` não estiver disponível, apenas `descricao` será usada.
* Os dados precisam ser convertidos em formato binário (0 ou 1) antes de aplicar o Apriori.

---

## Contato

Desenvolvido por: Artenio Resi
Email:artnioreis@live.com
