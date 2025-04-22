import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta
import random

def generate_fake_price_data(product_name="iPhone 14", days=10, current_price=None):
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in reversed(range(days))]

    base_price = current_price if current_price else 80000
    prices = [base_price - random.randint(0, 5000) for _ in range(days - 1)] + [current_price]

    df = pd.DataFrame({"Date": dates, "Price": prices})
    filename = f"{product_name.lower().replace(' ', '_')}_prices.csv"
    df.to_csv(filename, index=False)
    return filename

def predict_price(csv_file):
    try:
        df = pd.read_csv(csv_file)
        df = df.dropna()
        df["Price"] = df["Price"].astype(float)  # Use "Price" with capital P
        df["day"] = np.arange(len(df))

        if len(df) < 2:
            return df["Price"].iloc[-1], "Not enough data to predict"

        model = LinearRegression()
        model.fit(df[["day"]], df["Price"])

        next_day = [[len(df)]]
        predicted_price = model.predict(next_day)[0]

        current_price = df["Price"].iloc[-1]

        if predicted_price > current_price:
            decision = "Buy now – price may go up!"
        else:
            decision = "Wait – price may drop further."

        return round(predicted_price, 2), decision

    except Exception as e:
        print("❌ Prediction Error:", e)
        return 0.0, "Prediction failed"



def run_price_prediction(product_name, product_list):
    # Extract the first available price from Amazon, Flipkart, or eBay
    platforms = ["Amazon", "Flipkart", "eBay"]
    current_price = None

    for platform in platforms:
        for product in product_list:
            if product.get("Source") == platform and product.get("Price"):
                try:
                    price_clean = product['Price'].replace('₹', '').replace('$', '').replace(',', '').split()[0]
                    current_price = float(price_clean)
                    break
                except:
                    continue
        if current_price:
            break

    if not current_price:
        current_price = 80000  # fallback base price

    csv_file = generate_fake_price_data(product_name, current_price=current_price)
    return predict_price(csv_file)

if __name__ == "__main__":
    test_data = [
        {"Product Name": "iPhone 14", "Price": "₹74,999", "Source": "Amazon"},
        {"Product Name": "iPhone 14", "Price": "₹73,499", "Source": "Flipkart"},
        {"Product Name": "iPhone 14", "Price": "$699.99", "Source": "eBay"},
    ]
    predicted, advice = run_price_prediction("iPhone 14", test_data)
    print(f"📈 Predicted Price: ₹{predicted}")
    print(f"💡 Suggestion: {advice}")
