# app.py

from flask import Flask, render_template, request
from models import get_transactions
from services import prepare_data, run_apriori, plot_top_products, plot_confidence_vs_lift, suggest_kits

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    mensagem_erro = None
    df = None
    top_products_chart = None
    confidence_lift_chart = None
    kits = None
    metrics = None

    if request.method == 'POST':
        data_inicio = request.form.get('data_inicio', '2007-02-01')
        data_fim = request.form.get('data_fim', '2025-09-18')

        # Obtém transações do banco
        df = get_transactions(data_inicio, data_fim)

        # Verifica se houve erro retornado pelo DataFrame
        if 'erro' in df.columns:
            mensagem_erro = df['erro'].iloc[0]
            df = None
        else:
            try:
                basket = prepare_data(df)
                conjuntos, regras = run_apriori(basket, min_support=0.05)
                top_products_chart = plot_top_products(df)
                confidence_lift_chart = plot_confidence_vs_lift(regras)
                kits = suggest_kits(regras)
                metrics = {
                    'suporte': 0.05,
                    'confianca': 0.6,  # exemplo, calcule a partir das regras se quiser
                    'lift': 1.2         # exemplo, calcule a partir das regras se quiser
                }
            except Exception as e:
                mensagem_erro = f'Erro ao processar os dados: {e}'
                df = None

    return render_template(
        'index.html',
        mensagem_erro=mensagem_erro,
        top_products_chart=top_products_chart,
        confidence_lift_chart=confidence_lift_chart,
        kits=kits,
        metrics=metrics
    )

if __name__ == '__main__':
    app.run(debug=True)