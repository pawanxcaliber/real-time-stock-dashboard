from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return jsonify(message="Hello from Stock API!")


# Basic endpoint expected by the health check (will need more later)
@app.route('/health')
def health_check():
    return jsonify(status="UP"), 200


# Placeholder for stock data endpoint
@app.route('/stock/<symbol>')
def get_stock_price(symbol):
    # TODO: Implement fetching real stock data
    return jsonify(symbol=symbol, price=100.0, timestamp="placeholder")


if __name__ == '__main__':
    # Running directly for development - Gunicorn/production server later
    app.run(host='0.0.0.0', port=8000, debug=True)
