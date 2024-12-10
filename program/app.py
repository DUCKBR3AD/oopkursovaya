from flask import Flask, request, render_template_string

app = Flask(__name__)

materials = {
    "Дерево": 1000,
    "Металл": 1500,
    "Пластик": 500
}

furniture_types = {
    "Шкаф": 5000,
    "Стол": 3000,
    "Полка": 2000,
    "Тумбочка": 2500,
    "Контейнер": 1000,
    "Стеллаж": 4000
}

def calculate_total_cost(items):
    total_cost = 0
    detailed_items = []
    for item in items:
        material_cost = materials.get(item["material"], 0)
        furniture_cost = furniture_types.get(item["furniture_type"], 0)
        quantity = item["quantity"]
        item_cost = (material_cost + furniture_cost) * quantity
        total_cost += item_cost
        detailed_items.append({
            "material": item["material"],
            "furniture_type": item["furniture_type"],
            "quantity": quantity,
            "material_cost": material_cost,
            "furniture_cost": furniture_cost,
            "item_cost": item_cost
        })
    return total_cost, detailed_items


html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор стоимости производства мебели</title>
    <style>
        body {
            background-color: #808080;
            color: #ffffff;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .form-container {
            margin: 50px auto;
            padding: 20px;
            background-color: #444444;
            border-radius: 10px;
            width: 60%;
        }
        .item {
            margin-bottom: 20px;
            border-bottom: 1px solid #cccccc;
            padding-bottom: 10px;
        }
        select, input {
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #cccccc;
            width: 90%;
            max-width: 300px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: red;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: darkred;
        }
        h2, h3 {
            margin-top: 20px;
            color: #ffcc00;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
            text-align: left;
        }
        .footer {
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Калькулятор стоимости производства мебели</h1>
    <div class="form-container">
        <form action="/calculate" method="POST" id="furniture-form">
            <div id="items-container">
                <div class="item">
                    <label for="material">Выберите материал:</label><br>
                    <select name="material[]" required>
                        {% for material, cost in materials.items() %}
                            <option value="{{ material }}">{{ material }} ({{ cost }} руб.)</option>
                        {% endfor %}
                    </select><br>
                    <label for="furniture_type">Выберите тип мебели:</label><br>
                    <select name="furniture_type[]" required>
                        {% for furniture, cost in furniture_types.items() %}
                            <option value="{{ furniture }}">{{ furniture }} ({{ cost }} руб.)</option>
                        {% endfor %}
                    </select><br>
                    <label for="quantity">Количество:</label><br>
                    <input type="number" name="quantity[]" min="1" value="1" required>
                </div>
            </div>
            <button type="button" onclick="addItem()">Добавить ещё мебель</button>
            <br><br>
            <button type="submit">Рассчитать</button>
        </form>
        {% if total_cost is not none %}
            <div>
                <h2>Результаты расчета:</h2>
                <ul>
                    {% for item in detailed_items %}
                        <li>
                            {{ item.quantity }}x {{ item.material }} {{ item.furniture_type }}: 
                            {{ item.item_cost }} руб. 
                            (Материал: {{ item.material_cost }} руб., Мебель: {{ item.furniture_cost }} руб.)
                        </li>
                    {% endfor %}
                </ul>
                <h3>Общая стоимость: {{ total_cost }} руб.</h3>
                {% if discounted_cost is not none %}
                    <h3>Стоимость со скидкой (15%): {{ discounted_cost }} руб.</h3>
                {% endif %}
                <br>
                <form action="/" method="GET">
                    <button type="submit">Сделать новый расчет</button>
                </form>
            </div>
        {% endif %}
    </div>
    <div class="footer">
        Авторы: Яшкин Г.А. и Николаев В.Р., группа ПИ-300Б
    </div>
    <script>
        function addItem() {
            const container = document.getElementById('items-container');
            const newItem = document.createElement('div');
            newItem.className = "item";
            newItem.innerHTML = `
                <label for="material">Выберите материал:</label><br>
                <select name="material[]" required>
                    {% for material, cost in materials.items() %}
                        <option value="{{ material }}">{{ material }} ({{ cost }} руб.)</option>
                    {% endfor %}
                </select><br>
                <label for="furniture_type">Выберите тип мебели:</label><br>
                <select name="furniture_type[]" required>
                    {% for furniture, cost in furniture_types.items() %}
                        <option value="{{ furniture }}">{{ furniture }} ({{ cost }} руб.)</option>
                    {% endfor %}
                </select><br>
                <label for="quantity">Количество:</label><br>
                <input type="number" name="quantity[]" min="1" value="1" required>
            `;
            container.appendChild(newItem);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, materials=materials, furniture_types=furniture_types)

@app.route('/calculate', methods=['POST'])
def calculate():
    items = []
    materials_form = request.form.getlist("material[]")
    furniture_types_form = request.form.getlist("furniture_type[]")
    quantities_form = request.form.getlist("quantity[]")
    
    for material, furniture_type, quantity in zip(materials_form, furniture_types_form, quantities_form):
        items.append({
            "material": material,
            "furniture_type": furniture_type,
            "quantity": int(quantity)
        })
    
    total_cost, detailed_items = calculate_total_cost(items)
    discounted_cost = None
    if total_cost >= 20000:
        discounted_cost = round(total_cost * 0.85)
    
    return render_template_string(
        html_template,
        materials=materials,
        furniture_types=furniture_types,
        total_cost=total_cost,
        discounted_cost=discounted_cost,
        detailed_items=detailed_items
    )

if __name__ == "__main__":
    app.run(debug=True)

