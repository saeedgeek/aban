from flask import Flask, request, jsonify

app = Flask(__name__)

# لیست جهت ذخیره سفارشات
orders = []


@app.route('/submit_order', methods=['POST'])
def submit_order():
    # دریافت مقادیر ورودی سفارش
    data = request.get_json()
    crypto_name = data.get('crypto_name')
    amount = data.get('amount')

    # بررسی معتبر بودن ورودی‌ها
    if not crypto_name or not amount:
        return jsonify({'error': 'Invalid input, crypto_name and amount are required.'}), 400

    # ایجاد سفارش جدید
    order = {
        'id': len(orders) + 1,
        'crypto_name': crypto_name,
        'amount': amount
    }
    orders.append(order)
    return jsonify({'message': 'Order submitted successfully!', 'order': order}), 201


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
