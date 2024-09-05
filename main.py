from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-news', methods=['POST'])
def get_news():
    # Retrieve JSON data from request
    data = request.get_json()
    symbols = data.get('symbols')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    api_key = data.get('api_key')

    if not symbols or not isinstance(symbols, list):
        return jsonify({"error": "Invalid or missing symbols list"}), 400
    if not start_date or not end_date or not api_key:
        return jsonify({"error": "Missing required parameters"}), 400

    # Function to fetch news from Finnhub
    def fetch_news(symbols, start_date, end_date, api_key):
        base_url = "https://finnhub.io/api/v1/company-news"
        news_results = {}
        for symbol in symbols:
            params = {
                'symbol': symbol,
                'from': start_date,
                'to': end_date,
                'token': api_key
            }
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                news_results[symbol] = response.json()
            except requests.RequestException as e:
                news_results[symbol] = {"error": str(e)}
        return news_results

    # Fetch and return the news
    results = fetch_news(symbols, start_date, end_date, api_key)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
