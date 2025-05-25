# Código para baixar as bibliotecas/frameworks pip install flask pulp
# Código para rodar: python app.py
# Bibliotecas/frameworks
from flask import Flask, render_template, request
import pulp

# Cria a aplicação Flask
app = Flask(__name__)

# Rota para maximização
@app.route('/maximizacao')
def maximizacao():
    return render_template('maximizacao.html') 

# Rota para minimização
@app.route('/minimizacao')
def minimizacao():
    return render_template('minimizacao.html') 


# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultadoMax', methods=['POST'])
def resultado_max():
    # Função objetiva
    lucro_a = float(request.form['lucro_a'])
    lucro_b = float(request.form['lucro_b'])

    # Restrição 1
    r1_a = float(request.form['r1_a'])
    r1_b = float(request.form['r1_b'])
    r1_limite = float(request.form['r1_limite'])

    # Restrição 2
    r2_a = float(request.form['r2_a'])
    r2_b = float(request.form['r2_b'])
    r2_limite = float(request.form['r2_limite'])

    # Modelo para maximização
    prob = pulp.LpProblem("Maximização_lucro", pulp.LpMaximize)

    A = pulp.LpVariable('A', lowBound=0, cat='Continuous')
    B = pulp.LpVariable('B', lowBound=0, cat='Continuous')

    # Função objetiva
    prob += lucro_a * A + lucro_b * B, "Lucro"

    # Restrições
    prob += r1_a * A + r1_b * B <= r1_limite, "Restricao1"
    prob += r2_a * A + r2_b * B <= r2_limite, "Restricao2"

    # Resolver
    prob.solve()

    # Exibição do resultado
    return render_template(
        'resultadoMax.html',
        valor_a=A.varValue,
        valor_b=B.varValue,
        lucro=pulp.value(prob.objective)
    )

@app.route('/resultadoMin', methods=['POST'])
def resultado_min():
    # Coeficientes da função objetivo
    coef_a = float(request.form['lucro_a'])
    coef_b = float(request.form['lucro_b'])

    # Restrição 1
    r1_a = float(request.form['r1_a'])
    r1_b = float(request.form['r1_b'])
    r1_limite = float(request.form['r1_limite'])

    # Restrição 2
    r2_a = float(request.form['r2_a'])
    r2_b = float(request.form['r2_b'])
    r2_limite = float(request.form['r2_limite'])

    # Mínimos de A e B definidos pelo usuário
    min_a = float(request.form['min_a'])
    min_b = float(request.form['min_b'])

    # Definição do problema
    prob = pulp.LpProblem("Minimizacao_Custo", pulp.LpMinimize)

    A = pulp.LpVariable('A', lowBound=0, cat='Continuous')
    B = pulp.LpVariable('B', lowBound=0, cat='Continuous')

    prob += coef_a * A + coef_b * B, "Custo"
    prob += r1_a * A + r1_b * B <= r1_limite, "Restrição1"
    prob += r2_a * A + r2_b * B <= r2_limite, "Restrição2"
    prob += A >= min_a, "MinA"
    prob += B >= min_b, "MinB"

    prob.solve()

    return render_template('resultadoMin.html',
                           quantidade_a=A.varValue,
                           quantidade_b=B.varValue,
                           custo=pulp.value(prob.objective),
                           status=pulp.LpStatus[prob.status])

# Inicia o servidor web
if __name__ == '__main__':
    app.run(debug=True)
