from flask import Flask, render_template, request

app = Flask(__name__)

nutritional_data = {
    "chicken":     {"calories": 165, "protein": 31,  "fat": 3.6,  "carbohydrates": 0, "sodium": 74},
    "beef":        {"calories": 250, "protein": 26,  "fat": 17,   "carbohydrates": 0, "sodium": 72},
    "salmon":      {"calories": 208, "protein": 20,  "fat": 13,   "carbohydrates": 0, "sodium": 59},
    "tilapia":     {"calories": 129, "protein": 26,  "fat": 2.7,  "carbohydrates": 0, "sodium": 56},
    "shrimp":      {"calories": 99,  "protein": 24,  "fat": 0.3,  "carbohydrates": 0.2, "sodium": 111},

    "sweet potato":  {"calories": 86,  "protein": 1.6, "fat": 0.1,  "carbohydrates": 20, "sodium": 55},
    "potato":  {"calories": 77,  "protein": 2,   "fat": 0.1,  "carbohydrates": 17, "sodium": 6},
    "red potato":    {"calories": 70,  "protein": 1.9, "fat": 0.1,  "carbohydrates": 15.9, "sodium": 10},
    "white rice":    {"calories": 130, "protein": 2.7, "fat": 0.3,  "carbohydrates": 28, "sodium": 1},
    "pasta":         {"calories": 160, "protein": 10,  "fat": 1.5,  "carbohydrates": 35, "sodium": 0},
    "quinoa":        {"calories": 120, "protein": 4.4, "fat": 1.9,  "carbohydrates": 21.3, "sodium": 7},
    "cauliflower":   {"calories": 25,  "protein": 1.9, "fat": 0.3,  "carbohydrates": 5, "sodium": 30},

    "broccoli":      {"calories": 55,  "protein": 3.7, "fat": 0.6,  "carbohydrates": 11, "sodium": 33},
    "zucchini":      {"calories": 17,  "protein": 1.2, "fat": 0.3,  "carbohydrates": 3.1, "sodium": 8},
    "asparagus":     {"calories": 20,  "protein": 2.2, "fat": 0.2,  "carbohydrates": 3.9, "sodium": 2},
    "brussels": {"calories": 43, "protein": 3.4, "fat": 0.3, "carbohydrates": 9, "sodium": 25},
    "spinach":       {"calories": 23,  "protein": 2.9, "fat": 0.4,  "carbohydrates": 3.6, "sodium": 79},
    "cucumber":      {"calories": 15,  "protein": 0.7, "fat": 0.1,  "carbohydrates": 3.6, "sodium": 2},
    "green beans":   {"calories": 31,  "protein": 1.8, "fat": 0.1,  "carbohydrates": 7, "sodium": 6},
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
