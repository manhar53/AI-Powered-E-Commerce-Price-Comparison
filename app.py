from flask import Flask, request, jsonify
from flask_cors import CORS
from Combining_All_Scrapers import run_scraper_and_get_data
from price_predictor import run_price_prediction
import pandas as pd
import math

app = Flask(__name__)
CORS(app)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    query = data.get("query")

    try:
        # Run scraping
        products, recommendation = run_scraper_and_get_data(query)

        # Clean NaN values for JSON compatibility
        df = pd.DataFrame(products)
        df.fillna("", inplace=True)

        # ✅ Limit to 5 products per platform
        df_limited = df.groupby("Source").head(5).reset_index(drop=True)

        # ✅ Sort by platform priority: Amazon > Flipkart > eBay
        platform_order = {"Amazon": 0, "Flipkart": 1, "eBay": 2}
        df_limited["platform_rank"] = df_limited["Source"].map(platform_order)
        df_limited = df_limited.sort_values(by="platform_rank").drop(columns="platform_rank")

        clean_products = df_limited.to_dict(orient="records")


        # Run prediction
        predicted_price, buy_decision = run_price_prediction(query, clean_products)

        return jsonify({
            "products": clean_products,
            "recommendation": recommendation,
            "prediction": {
                "predicted_price": f"₹{predicted_price}",
                "buy_decision": buy_decision
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
