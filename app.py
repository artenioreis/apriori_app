# app.py

from flask import Flask, render_template, request
from models import get_transactions
from services import prepare_data, run_apriori, explain_metrics, plot_top_products, plot_confidence_vs_lift, suggest_kits

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Valores padrão
    min_support = 0.05
    min_confidence = 0.5
    start_date = None
    end_date = None

    # Atualiza parâmetros com filtros do formulário
    if request.method == 'POST':
        min_support = float(request.form.get('min_support', 0.05))
        min_confidence = float(request.form.get('min_confidence', 0.5))
        start_date = request.form.get('start_date') or None
        end_date = request.form.get('end_date') or None

    # Carrega os dados do banco
    df = get_transactions(start_date, end_date)

    if df.empty:
        print("⚠️ Nenhum dado encontrado para o período selecionado")
        return render_template("index.html", no_data=True)

    print(f"📊 {len(df)} linhas carregadas do banco de dados")

    # Prepara os dados para Apriori
    basket = prepare_data(df)
    print(f"✅ Dados preparados: {basket.shape[0]} linhas x {basket.shape[1]} colunas")

    # Executa Apriori com min_support correto
    conjuntos_de_itens_frequentes, regras = run_apriori(basket, min_support=min_support)

    # Filtra regras pela confiança mínima
    regras = regras[regras['confidence'] >= min_confidence]
    print(f"✅ {len(regras)} regras após filtro de confiança >= {min_confidence}")

    # Gera gráficos
    top_products_chart = plot_top_products(df)
    confidence_lift_chart = plot_confidence_vs_lift(regras)

    # Sugere kits
    kit_suggestions = suggest_kits(regras, min_confidence=min_confidence)

    # Conceitos para exibir na interface
    metrics = explain_metrics()

    return render_template("index.html",
                           frequent_itemsets=conjuntos_de_itens_frequentes.to_html(classes="table table-striped"),
                           rules=regras.to_html(classes="table table-bordered"),
                           metrics=metrics,
                           top_products_chart=top_products_chart,
                           confidence_lift_chart=confidence_lift_chart,
                           kit_suggestions=kit_suggestions,
                           min_support=min_support,
                           min_confidence=min_confidence,
                           start_date=start_date,
                           end_date=end_date)

if __name__ == "__main__":
    app.run(debug=True)
