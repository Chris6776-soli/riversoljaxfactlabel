from flask import Flask, render_template, request

app = Flask(__name__)

nutritional_data = {
    "pollo":     {"calorias": 165, "proteina": 31,  "grasa": 3.6,  "carbohidratos": 0, "sodio": 74},
    "res":       {"calorias": 250, "proteina": 26,  "grasa": 17,   "carbohidratos": 0, "sodio": 72},
    "salmon":    {"calorias": 208, "proteina": 20,  "grasa": 13,   "carbohidratos": 0, "sodio": 59},
    "tilapia":   {"calorias": 129, "proteina": 26,  "grasa": 2.7,  "carbohidratos": 0, "sodio": 56},
    "camarones": {"calorias": 99,  "proteina": 24,  "grasa": 0.3,  "carbohidratos": 0.2, "sodio": 111},

    "boniato":   {"calorias": 86,  "proteina": 1.6, "grasa": 0.1,  "carbohidratos": 20, "sodio": 55},
    "papa_blanca": {"calorias": 77, "proteina": 2,   "grasa": 0.1,  "carbohidratos": 17, "sodio": 6},
    "papa_roja": {"calorias": 70,  "proteina": 1.9, "grasa": 0.1,  "carbohidratos": 15.9, "sodio": 10},
    "arroz":     {"calorias": 130, "proteina": 2.7, "grasa": 0.3,  "carbohidratos": 28, "sodio": 1},
    "pasta":     {"calorias": 160, "proteina": 10,  "grasa": 1.5,  "carbohidratos": 35, "sodio": 0},
    "quinoa":    {"calorias": 120, "proteina": 4.4, "grasa": 1.9,  "carbohidratos": 21.3, "sodio": 7},
    "coliflor":  {"calorias": 25,  "proteina": 1.9, "grasa": 0.3,  "carbohidratos": 5, "sodio": 30},

    "brocoli":   {"calorias": 55,  "proteina": 3.7, "grasa": 0.6,  "carbohidratos": 11, "sodio": 33},
    "zuchini":   {"calorias": 17,  "proteina": 1.2, "grasa": 0.3,  "carbohidratos": 3.1, "sodio": 8},
    "esparragos": {"calorias": 20, "proteina": 2.2, "grasa": 0.2,  "carbohidratos": 3.9, "sodio": 2},
    "coles":     {"calorias": 43,  "proteina": 3.4, "grasa": 0.3,  "carbohidratos": 9, "sodio": 25},
    "espinacas": {"calorias": 23,  "proteina": 2.9, "grasa": 0.4,  "carbohidratos": 3.6, "sodio": 79},
    "pepino":    {"calorias": 15,  "proteina": 0.7, "grasa": 0.1,  "carbohidratos": 3.6, "sodio": 2},
    "green_beans": {"calorias": 31,"proteina": 1.8, "grasa": 0.1,  "carbohidratos": 7, "sodio": 6},
}

def calcular_etiqueta(ingredientes):
    total = {"calorias": 0, "proteina": 0, "grasa": 0, "carbohidratos": 0, "sodio": 0}
    for tipo, data in ingredientes.items():
        nombre = data['nombre']
        gramos = data['gramos']
        if nombre in nutritional_data and gramos > 0:
            factor = gramos / 100
            for key in total:
                total[key] += nutritional_data[nombre][key] * factor
    return total

@app.route('/', methods=['GET', 'POST'])
def index():
    etiqueta = None
    resumen = []
    if request.method == 'POST':
        ingredientes = {
            'proteina': {
                'nombre': request.form.get('proteina'),
                'gramos': float(request.form.get('proteina_gramos') or 0) * 28.35
            },
            'carbohidrato': {
                'nombre': request.form.get('carbohidrato'),
                'gramos': float(request.form.get('carbohidrato_gramos') or 0) * 28.35
            },
            'vegetal': {
                'nombre': request.form.get('vegetal'),
                'gramos': float(request.form.get('vegetal_gramos') or 0) * 28.35
            },
        }
        etiqueta = calcular_etiqueta(ingredientes)

        for tipo, data in ingredientes.items():
            nombre = data['nombre']
            onzas = round(data['gramos'] / 28.35)
            if nombre and onzas > 0:
                resumen.append(f"{nombre.capitalize()} {onzas}oz")

    return render_template('index.html', etiqueta=etiqueta, resumen=', '.join(resumen))

if __name__ == '__main__':
    app.run(debug=True)