# services.py

import pandas as pd
import unicodedata
from mlxtend.frequent_patterns import apriori, association_rules
import plotly.express as px

# Remove acentos das colunas e strings
def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str)
        if unicodedata.category(c) != 'Mn'
    )

# Prepara os dados para Apriori
def prepare_data(df):
    print("📊 Colunas originais:", df.columns.tolist())
    df.columns = [remove_accents(col).lower().strip() for col in df.columns]
    print("✅ Colunas após padronização:", df.columns.tolist())

    if 'codigo' in df.columns:
        # Agrupa transações por código + descrição
        basket = (df.groupby(['codigo', 'descricao'])['descricao']
                    .count().unstack()
                    .reset_index()
                    .fillna(0))
    else:
        # Agrupa por descrição apenas
        basket = (df.groupby(['descricao'])['descricao']
                    .count()
                    .reset_index()
                    .fillna(0))
    
    # 🔹 TRANSFORMA EM BINÁRIO (0 ou 1) para o Apriori
    def encode_units(x):
        return 1 if x >= 1 else 0

    basket_bin = basket.applymap(encode_units)
    
    print("✅ Basket transformado em binário para Apriori")
    return basket_bin


# Executa Apriori com min_support como argumento
def run_apriori(basket, min_support=0.05, metric='lift', min_threshold=1):
    print(f"▶ Rodando Apriori com min_support={min_support}, metric={metric}, min_threshold={min_threshold}")
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    print(f"✅ {len(frequent_itemsets)} itemsets frequentes encontrados")

    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    print(f"✅ {len(rules)} regras geradas")
    return frequent_itemsets, rules

# Explica métricas usadas
def explain_metrics():
    return {
        "suporte": "Proporção de transações que contêm o item ou combinação de itens.",
        "confianca": "Probabilidade de encontrar o item consequente dado que o antecedente está presente.",
        "lift": "Mede a força da associação. Lift > 1 indica que a presença do antecedente aumenta a probabilidade do consequente."
    }

# Gráfico dos produtos mais vendidos
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

# Gráfico Confiança x Lift
def plot_confidence_vs_lift(rules):
    fig = px.scatter(
        rules,
        x='confidence',
        y='lift',
        hover_data=['antecedents', 'consequents'],
        title="Relação entre Confiança e Lift"
    )
    return fig.to_html(full_html=False)

# Sugestão de kits com base nas regras
def suggest_kits(rules, min_confidence=0.5):
    kits = rules[rules['confidence'] >= min_confidence][['antecedents', 'consequents', 'confidence', 'lift']]
    kits = kits.sort_values(by='lift', ascending=False)
    return kits