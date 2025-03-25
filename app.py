from flask import Flask, jsonify
from utils.shopify_helpers import get_free_gift_products

app = Flask(__name__)

@app.route('/')
def home():
    return 'Free Gift App is running!'

@app.route('/gifts')
def gifts():
    products = get_free_gift_products()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
