# app.py

from flask import Flask, render_template, request
from models import get_transactions
from services import prepare_data, run_apriori, plot_top_products, plot_confidence_vs_lift, suggest_kits, explain_metrics

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Inicializa todas as variáveis que o template pode precisar
    mensagem_erro = None
    top_products_chart = None
    confidence_lift_chart = None
    frequent_itemsets = None
    rules = None
    kit_suggestions = None
    no_data = False
    
    # Valores padrão para os campos do formulário
    start_date = '2007-02-01'
    end_date = '2025-09-18'
    min_support = 0.05
    min_confidence = 0.5
    
    metrics = explain_metrics() # Pega a explicação das métricas

    if request.method == 'POST':
        # Atualiza os valores com base no que foi enviado pelo formulário
        start_date = request.form.get('start_date', start_date)
        end_date = request.form.get('end_date', end_date)
        min_support = float(request.form.get('min_support', min_support))
        min_confidence = float(request.form.get('min_confidence', min_confidence))

        try:
            # 1. Obter transações do banco
            df = get_transactions(start_date, end_date)

            # 2. Verificar se houve erro retornado pela função get_transactions
            if 'erro' in df.columns:
                mensagem_erro = df['erro'].iloc[0]
            
            # 3. Se não houver dados, definir a flag no_data
            elif df.empty:
                no_data = True
            
            # 4. Se houver dados e nenhum erro, processar
            else:
                basket = prepare_data(df)
                frequent_itemsets_df, rules_df = run_apriori(basket, min_support=min_support)
                
                top_products_chart = plot_top_products(df)
                confidence_lift_chart = plot_confidence_vs_lift(rules_df)
                kit_suggestions = suggest_kits(rules_df, min_confidence=min_confidence)

                # Converter dataframes para HTML para exibição
                frequent_itemsets = frequent_itemsets_df.to_html(classes='table table-striped', index=False)
                rules = rules_df.to_html(classes='table table-striped', index=False)


        except Exception as e:
            # Captura qualquer outro erro inesperado durante o processo
            mensagem_erro = f'Ocorreu um erro inesperado ao processar os dados: {e}'

    return render_template('index.html',
                           mensagem_erro=mensagem_erro,
                           top_products_chart=top_products_chart,
                           confidence_lift_chart=confidence_lift_chart,
                           frequent_itemsets=frequent_itemsets,
                           rules=rules,
                           kit_suggestions=kit_suggestions,
                           no_data=no_data,
                           metrics=metrics,
                           start_date=start_date,
                           end_date=end_date,
                           min_support=min_support,
                           min_confidence=min_confidence)


if __name__ == '__main__':
    app.run(debug=True)