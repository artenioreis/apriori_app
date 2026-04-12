# services.py

import pandas as pd
import unicodedata
# --- INÍCIO DA OTIMIZAÇÃO DE MEMÓRIA ---
# Importa o TransactionEncoder, que é a ferramenta correta para transformar os dados
# de forma eficiente quando se tem muitas transações.
from mlxtend.preprocessing import TransactionEncoder
# --- FIM DA OTIMIZAÇÃO DE MEMÓRIA ---
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px

# Função para remover acentos (não foi alterada)
def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

# --- INÍCIO DA OTIMIZAÇÃO DE MEMÓRIA ---
# Prepara os dados para o formato de cesta de compras usando um método eficiente.
def prepare_data(df):
    # 1. Agrupa os produtos por nota fiscal. Em vez de criar uma tabela gigante,
    #    isto cria uma lista de listas, onde cada lista interna contém os produtos de uma única venda.
    #    Ex: [['Pão', 'Manteiga'], ['Café', 'Açúcar'], ['Pão', 'Leite']]
    print("Agrupando produtos por transação...")
    transactions = df.groupby('num_nota')['descricao'].apply(list).tolist()

    # 2. Usa o TransactionEncoder para transformar a lista de transações numa matriz binária.
    #    Este método é otimizado e consome muito menos memória do que o .unstack().
    print("Codificando transações para o formato binário...")
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)

    # 3. Converte a matriz resultante de volta para um DataFrame do pandas.
    basket_bin = pd.DataFrame(te_ary, columns=te.columns_)

    print("✅ Basket transformado em binário para Apriori (método otimizado)")
    return basket_bin
# --- FIM DA OTIMIZAÇÃO DE MEMÓRIA ---


# Executa o algoritmo Apriori (não foi alterado)
def run_apriori(basket, min_support=0.05, metric='lift', min_threshold=1):
    print(f"▶ Rodando Apriori com min_support={min_support}, metric={metric}, min_threshold={min_threshold}")
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    print(f"✅ {len(frequent_itemsets)} itemsets frequentes encontrados")

    if frequent_itemsets.empty:
        print("⚠️ Nenhum itemset frequente encontrado com o suporte mínimo fornecido.")
        return frequent_itemsets, pd.DataFrame(columns=['antecedents', 'consequents', 'support', 'confidence', 'lift'])

    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    print(f"✅ {len(rules)} regras geradas")
    return frequent_itemsets, rules

# Retorna explicações das métricas (não foi alterado)
def explain_metrics():
    return {
        "suporte": "Proporção de transações que contêm o item ou combinação de itens.",
        "confianca": "Probabilidade de encontrar o item consequente dado que o antecedente está presente.",
        "lift": "Mede a força da associação. Lift > 1 indica que a presença do antecedente aumenta a probabilidade do consequente."
    }

# Gera o gráfico dos produtos mais vendidos (não foi alterado)
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

# Gera o gráfico de Confiança vs. Lift (não foi alterado)
def plot_confidence_vs_lift(rules):
    rules_for_plot = rules.copy()
    rules_for_plot['antecedents'] = rules_for_plot['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules_for_plot['consequents'] = rules_for_plot['consequents'].apply(lambda x: ', '.join(list(x)))

    fig = px.scatter(
        rules_for_plot,
        x='confidence',
        y='lift',
        hover_data=['antecedents', 'consequents'],
        title="Relação entre Confiança e Lift"
    )
    return fig.to_html(full_html=False)

# Sugere kits de produtos (não foi alterado)
def suggest_kits(rules):
    kits = rules[['antecedents', 'consequents', 'confidence', 'lift']]
    kits['antecedents'] = kits['antecedents'].apply(lambda x: ', '.join(list(x)))
    kits['consequents'] = kits['consequents'].apply(lambda x: ', '.join(list(x)))
    kits = kits.sort_values(by='lift', ascending=False)
    return kits

