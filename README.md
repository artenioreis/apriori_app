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
* Os dados precisam ser convertidos em formato binário (0 ou 1) antes de aplicar o Apriori

Claro, aqui está uma análise detalhada de cada arquivo no projeto:

### `README.md`
Este arquivo serve como um guia completo para o projeto "Apriori App". Ele descreve o propósito do aplicativo, que é a análise de dados de vendas usando o algoritmo Apriori para identificar padrões de compra.

O `README.md` detalha as principais funcionalidades do sistema:
* Conexão com um banco de dados SQL Server.
* Preparação e processamento de dados para a análise.
* Execução do algoritmo Apriori com parâmetros ajustáveis.
* Geração de regras de associação e sugestão de kits de produtos.
* Visualização de dados através de gráficos interativos.

Além disso, o arquivo fornece um passo a passo para a instalação, incluindo como clonar o repositório, configurar um ambiente virtual e instalar as dependências necessárias listadas no `requirements.txt`. Ele também explica como executar a aplicação Flask e como acessá-la em um navegador da web.

A estrutura do projeto é claramente delineada, mostrando a organização dos arquivos e suas respectivas funções. Por fim, o `README.md` lista as dependências do projeto e oferece informações de contato do desenvolvedor, Artenio Reis.

### `app.py`
Este é o arquivo principal da aplicação Flask. Ele é responsável por gerenciar as rotas e a lógica de interação com o usuário.

O `app.py` define uma única rota (`/`) que aceita tanto requisições `GET` quanto `POST`.
* Quando a página é carregada pela primeira vez (uma requisição `GET`), a interface é exibida sem dados.
* Quando o usuário submete o formulário com as datas e os parâmetros (uma requisição `POST`), o `app.py` coordena as seguintes ações:
    1.  Chama a função `get_transactions` do `models.py` para buscar os dados de vendas do banco de dados.
    2.  Verifica se os dados foram retornados com sucesso; caso contrário, exibe uma mensagem de erro.
    3.  Se os dados estiverem corretos, ele utiliza as funções do `services.py` para:
        * Preparar os dados com `prepare_data`.
        * Executar o algoritmo Apriori com `run_apriori`.
        * Gerar os gráficos com `plot_top_products` e `plot_confidence_vs_lift`.
        * Sugerir kits de produtos com `suggest_kits`.
    4.  As informações processadas são então enviadas para o `index.html` para serem exibidas na interface do usuário.

Este arquivo também inicializa a aplicação Flask e a executa em modo de depuração, o que facilita o desenvolvimento e a identificação de erros.

### `models.py`
Este arquivo é responsável pela comunicação com o banco de dados SQL Server. Ele contém a função `get_transactions`, que busca os dados de vendas.

A função `get_transactions` realiza as seguintes tarefas:
1.  **Configura a Conexão**: Define a string de conexão para o banco de dados, incluindo detalhes como o driver, servidor, nome do banco, usuário e senha.
2.  **Estabelece a Conexão**: Tenta se conectar ao banco de dados usando a biblioteca `pyodbc`. Se a conexão falhar, ele retorna um DataFrame do pandas com uma mensagem de erro.
3.  **Executa a Consulta SQL**: Realiza uma consulta para selecionar o código e a descrição dos produtos das tabelas `NFSIT` e `PRODU`. A junção das tabelas (`INNER JOIN`) garante que apenas os produtos que existem em ambas as tabelas sejam retornados.
4.  **Trata Erros**: Se ocorrer um erro durante a execução da consulta, a função retorna um DataFrame com uma mensagem de erro.
5.  **Fecha a Conexão**: Garante que a conexão com o banco de dados seja fechada após a conclusão da consulta, liberando os recursos.
6.  **Retorna os Dados**: Se a consulta for bem-sucedida, a função retorna os dados em um DataFrame do pandas.

### `services.py`
Este arquivo contém a lógica de negócio da aplicação, incluindo o pré-processamento dos dados, a execução do algoritmo Apriori e a criação dos gráficos.

As principais funções do `services.py` são:
* **`remove_accents`**: Uma função utilitária para remover acentos de strings, usada para padronizar os nomes das colunas.
* **`prepare_data`**: Prepara os dados brutos para a análise. Ela padroniza os nomes das colunas (removendo acentos e convertendo para minúsculas), agrupa os produtos por transação e transforma os dados em um formato binário (onde `1` indica a presença de um item em uma transação e `0` a ausência), que é o formato exigido pelo algoritmo Apriori.
* **`run_apriori`**: Executa o algoritmo Apriori para encontrar conjuntos de itens frequentes e, em seguida, gera as regras de associação com base nesses conjuntos. Os parâmetros `min_support`, `metric` e `min_threshold` permitem ajustar a sensibilidade do algoritmo.
* **`explain_metrics`**: Retorna um dicionário com explicações sobre as métricas do Apriori (suporte, confiança e lift).
* **`plot_top_products`**: Cria um gráfico de barras com os produtos mais vendidos, utilizando a biblioteca `plotly.express`.
* **`plot_confidence_vs_lift`**: Gera um gráfico de dispersão que mostra a relação entre a confiança e o lift das regras de associação.
* **`suggest_kits`**: Filtra as regras de associação para sugerir combinações de produtos (kits) com base em um valor mínimo de confiança, ordenando-as pelo lift para destacar as associações mais fortes.

### `config.py`
Este arquivo é usado para centralizar as configurações de conexão com o banco de dados. Ele define um dicionário chamado `DB_CONFIG` que contém todos os parâmetros necessários para a conexão, como o driver, servidor, nome do banco, usuário e senha. No entanto, é importante notar que, no arquivo `models.py`, a string de conexão é definida diretamente, o que sugere que o `config.py` pode não estar sendo utilizado na versão atual do código.

### `requirements.txt`
Este arquivo lista todas as bibliotecas Python de que o projeto depende. Ele é usado para garantir que o ambiente de desenvolvimento seja consistente e que todas as dependências possam ser instaladas facilmente com um único comando (`pip install -r requirements.txt`). As dependências listadas são:
* `Flask`: O framework web usado para construir a aplicação.
* `pandas`: Para manipulação e análise de dados.
* `pyodbc`: Para a conexão com o banco de dados SQL Server.
* `mlxtend`: Contém a implementação do algoritmo Apriori.

### `templates/index.html`
Este arquivo define a estrutura da interface do usuário da aplicação. Ele utiliza a sintaxe do Jinja2, o motor de templates do Flask, para exibir os dados dinamicamente.

O `index.html` inclui:
* Um formulário onde o usuário pode inserir as datas de início e fim, o suporte mínimo e a confiança mínima para a análise.
* Seções para exibir os resultados, incluindo:
    * As definições das métricas do Apriori.
    * O gráfico dos produtos mais vendidos.
    * Os conjuntos de itens frequentes.
    * As regras de associação.
    * As sugestões de kits de produtos.
    * O gráfico de confiança vs. lift.
* Uma mensagem de aviso é exibida se nenhum dado for encontrado para o período selecionado.
* A página utiliza o Bootstrap para estilização, o que garante uma aparência moderna e responsiva.

### `static/style.css`
Este arquivo contém as regras de estilo CSS personalizadas para a aplicação, complementando o Bootstrap. Ele define a aparência de elementos como o corpo da página, o cabeçalho, os formulários, as tabelas e os contêineres dos gráficos, garantindo uma identidade visual consistente para a aplicação.

### `__pycache__/`
Este diretório contém versões compiladas dos arquivos Python (`.pyc`). O Python cria esses arquivos automaticamente para acelerar o tempo de carregamento dos módulos. Eles não são relevantes para a lógica principal do código, e geralmente são ignorados em sistemas de controle de versão como o Git.

## Contato

Desenvolvido por: Artenio Resi
Email:artnioreis@live.com    

         www.linkedin.com/in/artenioreiss
