from flask import *


currencyy = Blueprint('currencyy', __name__)

CONVERSION_RATES = {
    "USD":0.012,
    "GBP":0.0095,
    "AED":0.044,
    "JPY":1.78,
    "AUD":0.018,
    "JMD":1.81,
    "CAD":0.016,
    "EUR":0.011,
    "SGD":0.016,
    "NPR":1.6,
    "BDT":1.3,
    "LKR":3.6,
}
@currencyy.route('/currency', methods=['POST'])
def currency():
    data = request.get_json()
    base = data.get("BasePrice")
    currency = data.get("Currency")

    if currency not in CONVERSION_RATES:
        return jsonify({"error": "Unsupported currency"}), 400

    rate = CONVERSION_RATES[currency]
    rate = base * rate
    return jsonify({
        "currency": currency,
        "rate": rate
    })

@currencyy.route('/typeahead', methods=['GET'])
def Currency_Typeahead():
    return jsonify(list(CONVERSION_RATES.keys()))