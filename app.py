# app.py

# Importa as bibliotecas necessárias
from flask import Flask, render_template, request
from models import get_transactions
from services import (
    prepare_data, 
    run_apriori, 
    plot_top_products, 
    plot_confidence_vs_lift, 
    suggest_kits,
    explain_metrics,
    remove_accents # Importa a função para padronizar nomes de colunas
)
from datetime import date, timedelta

# Inicializa a aplicação Flask.
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # --- 1. Inicialização de Variáveis ---
    mensagem_erro = None
    no_data_from_db = False
    top_products_chart = None
    confidence_lift_chart = None
    frequent_itemsets_html = None
    rules_html = None
    kit_suggestions_html = None
    metrics = explain_metrics()

    # --- 2. Definição dos Valores Padrão do Formulário ---
    start_date = request.form.get('start_date', (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.form.get('end_date', date.today().strftime('%Y-%m-%d'))
    min_support = request.form.get('min_support', '0.01')
    min_confidence = request.form.get('min_confidence', '0.1')
    
    # --- 3. Processamento do Formulário (Requisição POST) ---
    if request.method == 'POST':
        try:
            min_support_float = float(min_support)
            min_confidence_float = float(min_confidence)

            # --- 4. Busca e Validação dos Dados ---
            print(f"Buscando dados entre {start_date} e {end_date}...")
            df = get_transactions(start_date, end_date)

            if 'erro' in df.columns:
                mensagem_erro = df['erro'].iloc[0]
            elif df.empty:
                no_data_from_db = True
            else:
                # --- 5. Análise e Geração de Gráficos ---
                print("Dados recebidos. Preparando para análise...")

                # --- CORREÇÃO CRÍTICA ---
                # Padroniza os nomes das colunas (ex: 'Descricao' -> 'descricao')
                # ANTES de qualquer função de processamento ser chamada.
                df.columns = [remove_accents(col).lower().strip() for col in df.columns]
                print(f"✅ Colunas padronizadas: {df.columns.tolist()}")
                
                # Agora as funções receberão os nomes de colunas corretos.
                top_products_chart = plot_top_products(df)
                basket = prepare_data(df)
                frequent_itemsets, rules = run_apriori(basket, min_support=min_support_float, metric='lift', min_threshold=0)

                if not frequent_itemsets.empty:
                    frequent_itemsets_html = frequent_itemsets.to_html(classes='table table-striped', index=False, float_format='{:.4f}'.format)
                
                if not rules.empty:
                    rules_filtered = rules[rules['confidence'] >= min_confidence_float]
                    
                    if not rules_filtered.empty:
                        rules_html = rules_filtered.to_html(classes='table table-striped', index=False, float_format='{:.2f}'.format)
                        confidence_lift_chart = plot_confidence_vs_lift(rules_filtered)
                        kit_suggestions = suggest_kits(rules_filtered)
                        if not kit_suggestions.empty:
                             kit_suggestions_html = kit_suggestions.to_html(classes='table table-striped', index=False, float_format='{:.2f}'.format)

        except ValueError:
            mensagem_erro = "Erro: Suporte e Confiança Mínima devem ser valores numéricos."
        except Exception as e:
            mensagem_erro = f'Ocorreu um erro inesperado: {e}'

    # --- 6. Renderização da Página ---
    return render_template(
        'index.html',
        start_date=start_date,
        end_date=end_date,
        min_support=min_support,
        min_confidence=min_confidence,
        mensagem_erro=mensagem_erro,
        no_data=no_data_from_db,
        metrics=metrics,
        top_products_chart=top_products_chart,
        confidence_lift_chart=confidence_lift_chart,
        frequent_itemsets=frequent_itemsets_html,
        rules=rules_html,
        kit_suggestions=kit_suggestions_html
    )

if __name__ == '__main__':
    app.run(debug=True)

