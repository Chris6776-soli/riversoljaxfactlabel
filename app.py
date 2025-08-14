from flask import Flask, render_template, request

app = Flask(__name__)

nutritional_data = {
    "protein.": {"calories": 165, "protein": 30, "fat": 3.6, "carbohydrates": 0, "sodium": 50},
    "chicken": {"calories": 165, "protein": 30, "fat": 3.6, "carbohydrates": 0, "sodium": 50},
    "beef": {"calories": 250, "protein": 25, "fat": 17, "carbohydrates": 0, "sodium": 48},
    "salmon": {"calories": 206, "protein": 20, "fat": 13, "carbohydrates": 0, "sodium": 76},
    "tilapia": {"calories": 128, "protein": 26, "fat": 2.7, "carbohydrates": 0, "sodium": 165},
    "shrimp": {"calories": 99, "protein": 24, "fat": 0.3, "carbohydrates": 0.2, "sodium": 300},
    "pork": {"calories": 188, "protein": 21, "fat": 13, "carbohydrates": 0, "sodium": 77},
    "turkey": {"calories": 169, "protein": 29, "fat": 6, "carbohydrates": 0, "sodium": 50},
    "liver": {"calories": 191, "protein": 29, "fat": 6.5, "carbohydrates": 5, "sodium": 72},
    "bison": {"calories": 214.2, "protein": 18.7, "fat": 15, "carbohydrates": 0, "sodium": 49},

    "carbs.": {"calories": 71, "protein": 2.1, "fat": 0.2, "carbohydrates": 18, "sodium": 2},
    "sweet potato": {"calories": 92, "protein": 1.7, "fat": 0.2, "carbohydrates": 22, "sodium": 36},
    "potato": {"calories": 71, "protein": 2.1, "fat": 0.2, "carbohydrates": 18, "sodium": 2},
    "red potato": {"calories": 72, "protein": 2, "fat": 0.1, "carbohydrates": 18, "sodium": 20},
    "white rice": {"calories": 355, "protein": 2.2, "fat": 0.7, "carbohydrates": 31, "sodium": 1},
    "pasta": {"calories": 340, "protein": 17, "fat": 2, "carbohydrates": 68, "sodium": 1},
    "quinoa": {"calories": 320, "protein": 10, "fat": 2, "carbohydrates": 22, "sodium": 30},
    "cauliflower": {"calories": 25, "protein": 2, "fat": 0.3, "carbohydrates": 5, "sodium": 15},
    "basmati rice": {"calories": 129.8, "protein": 2.7, "fat": 0, "carbohydrates": 28.5, "sodium": 5},
    "brown rice": {"calories": 111.2, "protein": 2.3, "fat": 0, "carbohydrates": 23.5, "sodium": 5},

    "veggies.": {"calories": 35, "protein": 3, "fat": 0.4, "carbohydrates": 6, "sodium": 0},
    "broccoli": {"calories": 35, "protein": 3, "fat": 0.4, "carbohydrates": 6, "sodium": 0},
    "zucchini": {"calories": 18, "protein": 1.2, "fat": 0.4, "carbohydrates": 4, "sodium": 14},
    "asparagus": {"calories": 22, "protein": 2.4, "fat": 0, "carbohydrates": 4, "sodium": 4},
    "brussels": {"calories": 60, "protein": 4.3, "fat": 0.8, "carbohydrates": 12, "sodium": 25},
    "spinach": {"calories": 23, "protein": 2.9, "fat": 0.4, "carbohydrates": 3.8, "sodium": 74},
    "cucumber": {"calories": 16, "protein": 0.6, "fat": 0.1, "carbohydrates": 2.9, "sodium": 2},
    "green beans": {"calories": 35, "protein": 1.9, "fat": 0.2, "carbohydrates": 7.9, "sodium": 1},
    "cabbage": {"calories": 25, "protein": 1.3, "fat": 0.1, "carbohydrates": 5.8, "sodium": 18},
    "chard": {"calories": 21, "protein": 2, "fat": 0.2, "carbohydrates": 3, "sodium": 4},
    "kale": {"calories": 28, "protein": 1.9, "fat": 0.4, "carbohydrates": 5.6, "sodium": 23},
    "carrot": {"calories": 35, "protein": 0.8, "fat": 0.2, "carbohydrates": 8.2, "sodium": 58},

    "egg": {"calories": 78, "protein": 6.3, "fat": 5.3, "carbohydrates": 0.6, "sodium": 62},
    "avocado": {"calories": 275, "protein": 3.3, "fat": 24.8, "carbohydrates": 14.2, "sodium": 13.2},
    "salad": {"calories": 17, "protein": 0.3, "fat": 0, "carbohydrates": 3.3, "sodium": 10},

    "olive_oil": {"calories": 44, "protein": 0, "fat": 5, "carbohydrates": 0, "sodium": 0},
    "dressing": {"calories": 21.5, "protein": 0, "fat": 5, "carbohydrates": 0, "sodium": 0},
}

extra_items = {"egg", "avocado"}
sauce_items = {"olive_oil", "dressing"}

def calculate_label(ingredients):
    total = {"calories": 0, "protein": 0, "fat": 0, "carbohydrates": 0, "sodium": 0}
    for category, data in ingredients.items():
        name = data['name']
        amount = data['amount']
        if not name or amount <= 0:
            continue
        if name in extra_items or name in sauce_items:
            for key in total:
                total[key] += nutritional_data[name][key] * amount
        else:
            factor = amount / 100
            for key in total:
                total[key] += nutritional_data[name][key] * factor
    return {k: round(v, 2) for k, v in total.items()}

@app.route('/', methods=['GET', 'POST'])
def index():
    label = None
    summary = []

    if request.method == 'POST':
        ingredients = {
            'protein': {
                'name': request.form.get('protein'),
                'amount': float(request.form.get('protein_ounces') or 0) * 28.35
            },
            'carbohydrate': {
                'name': request.form.get('carbohydrate'),
                'amount': float(request.form.get('carbohydrate_ounces') or 0) * 28.35
            },
            'vegetable': {
                'name': request.form.get('vegetable'),
                'amount': float(request.form.get('vegetable_ounces') or 0) * 28.35
            }
        }

        # Extras (checkboxes with count)
        extras_selected = request.form.getlist('extra')
        for extra in extras_selected:
            count = float(request.form.get(f'extra_{extra}_count') or 0)
            ingredients[f'extra_{extra}'] = {
                'name': extra,
                'amount': count
            }

        # Sauce (dropdown with count)
        sauce = request.form.get('sauce')
        sauce_count = float(request.form.get('sauce_count') or 0)
        if sauce and sauce_count > 0:
            ingredients['sauce'] = {
                'name': sauce,
                'amount': sauce_count
            }

        label = calculate_label(ingredients)

        for category, data in ingredients.items():
            name = data['name']
            amount = data['amount']
            if not name or amount <= 0:
                continue
            if name in extra_items:
                amount_str = f"{int(amount)}" if amount == int(amount) else f"{amount:.2f}".rstrip('0').rstrip('.')
                summary.append(f"{name.title()} {amount_str}")
            elif name in sauce_items:
                continue
            else:
                ounces = amount / 28.35
                amount_str = f"{int(ounces)}" if ounces == int(ounces) else f"{ounces:.2f}".rstrip('0').rstrip('.')
                summary.append(f"{name.title()} {amount_str} oz")

    return render_template('index.html', label=label, summary=', '.join(summary))

if __name__ == '__main__':
    app.run(debug=True)
