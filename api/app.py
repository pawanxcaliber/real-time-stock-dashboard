from flask import Flask, jsonify
import os
from prometheus_client import generate_latest, Counter # <--- Import necessary classes

app = Flask(__name__)

# Define a simple counter metric
# 'http_requests_total' is the metric name
# 'Total number of HTTP requests' is the help text
# labels=['method', 'endpoint'] define dimensions for the metric
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests',
                        ['method', 'endpoint']) # <--- Define the counter metric

@app.route('/')
def hello_world():
    # Increment the counter for the root endpoint
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc() # <--- Increment metric on route hit
    return 'Hello from Stock API!'

@app.route('/health')
def health_check():
    # Increment the counter for the health endpoint
    REQUEST_COUNT.labels(method='GET', endpoint='/health').inc() # <--- Increment metric on route hit
    return jsonify(status="ok")

# <--- Add the /metrics endpoint
@app.route('/metrics')
def metrics():
    # Generate the latest state of all metrics and return as plain text
    return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}

# Add your /stock/<symbol> route here later when implementing real data fetching
@app.route('/stock/<symbol>')
def get_stock_price(symbol):
    # Increment the counter for the stock endpoint
    REQUEST_COUNT.labels(method='GET', endpoint='/stock/<symbol>').inc() # <--- Increment metric on route hit
    # Placeholder data - replace with actual data fetching later
    return jsonify({
        "symbol": symbol,
        "price": 150.00,
        "timestamp": "..."
    })


if __name__ == '__main__':
    # Ensure the Flask dev server binds to 0.0.0.0 to be accessible in Docker
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 8000))