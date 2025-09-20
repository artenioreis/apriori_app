# services.py

import pandas as pd
import unicodedata
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px

# Remove acentos das colunas e strings
def remove_accents(input_str):
    # Normaliza a string para separar caracteres e acentos, depois remove os acentos.
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

# Prepara os dados para o formato de cesta de compras exigido pelo Apriori.
def prepare_data(df):
    # Cria uma tabela onde cada linha é uma transação (num_nota) e cada coluna é um produto.
    # O valor 1 indica a presença do produto na transação.
    basket = (df.groupby(['num_nota', 'descricao'])
                .size().unstack(fill_value=0))

    # Garante que todos os valores sejam binários (0 ou 1).
    def encode_units(x):
        return 1 if x >= 1 else 0

    basket_bin = basket.map(encode_units)

    print("✅ Basket transformado em binário para Apriori")
    return basket_bin

# Executa o algoritmo Apriori para encontrar itemsets e regras de associação.
def run_apriori(basket, min_support=0.05, metric='lift', min_threshold=1):
    print(f"▶ Rodando Apriori com min_support={min_support}, metric={metric}, min_threshold={min_threshold}")
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    print(f"✅ {len(frequent_itemsets)} itemsets frequentes encontrados")

    if frequent_itemsets.empty:
        print("⚠️ Nenhum itemset frequente encontrado com o suporte mínimo fornecido.")
        # Retorna DataFrames vazios para evitar erros posteriores.
        return frequent_itemsets, pd.DataFrame(columns=['antecedents', 'consequents', 'support', 'confidence', 'lift'])

    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    print(f"✅ {len(rules)} regras geradas")
    return frequent_itemsets, rules

# Retorna um dicionário com as explicações das métricas do Apriori.
def explain_metrics():
    return {
        "suporte": "Proporção de transações que contêm o item ou combinação de itens.",
        "confianca": "Probabilidade de encontrar o item consequente dado que o antecedente está presente.",
        "lift": "Mede a força da associação. Lift > 1 indica que a presença do antecedente aumenta a probabilidade do consequente."
    }

# Gera o gráfico de barras com os produtos mais vendidos.
def plot_top_products(df, top_n=10):
    top_products = df['descricao'].value_counts().head(top_n).reset_index()
    top_products.columns = ['Produto', 'Quantidade']

    fig = px.bar(
        top_products,
        x='Produto',
        y='Quantidade',
        title=f"Top {top_n} Produtos Mais Vendidos",
        text='Quantidade'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    return fig.to_html(full_html=False)

# Gera o gráfico de dispersão de Confiança vs. Lift.
def plot_confidence_vs_lift(rules):
    # --- CORREÇÃO DO ERRO 'frozenset is not JSON serializable' ---
    # Cria uma cópia do DataFrame para não alterar o original.
    rules_for_plot = rules.copy()
    
    # Converte as colunas 'antecedents' e 'consequents' de frozenset para uma string legível.
    # Isso é necessário para que a biblioteca de gráficos (Plotly) possa exibir os dados no hover.
    rules_for_plot['antecedents'] = rules_for_plot['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules_for_plot['consequents'] = rules_for_plot['consequents'].apply(lambda x: ', '.join(list(x)))

    fig = px.scatter(
        rules_for_plot, # Usa o DataFrame com os dados convertidos.
        x='confidence',
        y='lift',
        hover_data=['antecedents', 'consequents'], # Agora os dados do hover são strings.
        title="Relação entre Confiança e Lift"
    )
    return fig.to_html(full_html=False)

# Formata as regras de associação para sugerir kits de produtos.
def suggest_kits(rules):
    kits = rules[['antecedents', 'consequents', 'confidence', 'lift']]
    # Converte os frozensets para uma string mais amigável para exibição na tabela.
    kits['antecedents'] = kits['antecedents'].apply(lambda x: ', '.join(list(x)))
    kits['consequents'] = kits['consequents'].apply(lambda x: ', '.join(list(x)))
    kits = kits.sort_values(by='lift', ascending=False)
    return kits

