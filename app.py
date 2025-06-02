from flask import Flask, render_template, request

app = Flask(__name__)

nutritional_data = {
    "protein.":     {"calories": 165, "protein": 30,  "fat": 3.6,  "carbohydrates": 0, "sodium": 50},
    "chicken":     {"calories": 165, "protein": 30,  "fat": 3.6,  "carbohydrates": 0, "sodium": 50},
    "beef":       {"calories": 250, "protein": 25,  "fat": 17,   "carbohydrates": 0, "sodium": 48},
    "salmon":      {"calories": 206, "protein": 20,  "fat": 13,   "carbohydrates": 0, "sodium": 76},
    "tilapia":     {"calories": 128, "protein": 26,  "fat": 2.7,  "carbohydrates": 0, "sodium": 165},
    "shrimp":      {"calories": 99,  "protein": 24,  "fat": 0.3,  "carbohydrates": 0.2, "sodium": 300},
    "pork":        {"calories": 188, "protein": 21,  "fat": 13,   "carbohydrates": 0, "sodium": 77},
    "turkey":      {"calories": 169, "protein": 29,  "fat": 6,   "carbohydrates": 0, "sodium": 50},

    "carbs.":   {"calories": 71,  "protein": 2.1,   "fat": 0.2,  "carbohydrates": 18, "sodium": 2},
    "sweet potato":  {"calories": 92,  "protein": 1.7, "fat": 0.2,  "carbohydrates": 22, "sodium": 36},
    "potato":        {"calories": 71,  "protein": 2.1,   "fat": 0.2,  "carbohydrates": 18, "sodium": 2},
    "red potato":    {"calories": 72,  "protein": 2, "fat": 0.1,  "carbohydrates": 18, "sodium": 20},
    "white rice":    {"calories": 355, "protein": 2.2, "fat": 0.7,  "carbohydrates": 31, "sodium": 1},
    "pasta":         {"calories": 340, "protein": 17,  "fat": 2,  "carbohydrates": 68, "sodium": 1},
    "quinoa":        {"calories": 320, "protein": 10, "fat": 2,  "carbohydrates": 22, "sodium": 30},
    "cauliflower":   {"calories": 25,  "protein": 2, "fat": 0.3,  "carbohydrates": 5, "sodium": 15},

    "veggies.":      {"calories": 35,  "protein": 3, "fat": 0.4,  "carbohydrates": 6, "sodium": 0},
    "broccoli":      {"calories": 35,  "protein": 3, "fat": 0.4,  "carbohydrates": 6, "sodium": 0},
    "zucchini":      {"calories": 18,  "protein": 1.2, "fat": 0.4,  "carbohydrates": 4, "sodium": 14},
    "asparagus":     {"calories": 22,  "protein": 2.4, "fat": 0,  "carbohydrates": 4, "sodium": 4},
    "brussels":      {"calories": 60, "protein": 4.3, "fat": 0.8, "carbohydrates": 12, "sodium": 25},
    "spinach":       {"calories": 23,  "protein": 2.9, "fat": 0.4,  "carbohydrates": 3.8, "sodium": 74},
    "cucumber":      {"calories": 16,  "protein": 0.6, "fat": 0.1,  "carbohydrates": 2.9, "sodium": 2},
    "green beans":   {"calories": 35,  "protein": 1.9, "fat": 0.2,  "carbohydrates": 7.9, "sodium": 1},
}

def calculate_label(ingredients):
    total = {"calories": 0, "protein": 0, "fat": 0, "carbohydrates": 0, "sodium": 0}
    for category, data in ingredients.items():
        name = data['name']
        grams = data['grams']
        if name in nutritional_data and grams > 0:
            factor = grams / 100
            for key in total:
                total[key] += nutritional_data[name][key] * factor
    # Round each nutritional value to 2 decimal places
    return {k: round(v, 2) for k, v in total.items()}

@app.route('/', methods=['GET', 'POST'])
def index():
    label = None
    summary = []
    if request.method == 'POST':
        ingredients = {
            'protein': {
                'name': request.form.get('protein'),
                'grams': float(request.form.get('protein_ounces') or 0) * 28.35
            },
            'carbohydrate': {
                'name': request.form.get('carbohydrate'),
                'grams': float(request.form.get('carbohydrate_ounces') or 0) * 28.35
            },
            'vegetable': {
                'name': request.form.get('vegetable'),
                'grams': float(request.form.get('vegetable_ounces') or 0) * 28.35
            },
        }
        label = calculate_label(ingredients)

        for category, data in ingredients.items():
            name = data['name']
            ounces = round(data['grams'] / 28.35, 2)  # two decimal places
            if name and ounces > 0:
                summary.append(f"{name.title()} {ounces}oz")

    return render_template('index.html', label=label, summary=', '.join(summary))

if __name__ == '__main__':
    app.run(debug=True)
