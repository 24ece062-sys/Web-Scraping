from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

CORS(app)


@app.route("/api/crypto")
def get_crypto():

    try:
        # Read cryptocurrency data from CSV
        df = pd.read_csv("crypto_prices.csv")

        # Remove empty rows
        df = df.dropna(how="all")

        # Get the latest 10 cryptocurrency records
        latest_data = df.tail(10)

        # Convert CSV data to JSON
        data = latest_data.to_dict(orient="records")

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":

    print("Backend server started!")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )