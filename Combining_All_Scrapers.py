from scrape_flipkart import scrape_flipkart
from scrape_ebay import scrape_ebay
from scrape_amazon import scrape_amazon
import pandas as pd

def recommend_lowest_price(products):
    prioritized_sources = ["Amazon", "Flipkart"]
    fallback_source = "eBay"

    def clean_price(p):
        try:
            raw = p.get("Price") or p.get("price") or ""
            return float(
                raw.replace("₹", "").replace("$", "").replace(",", "").strip().split()[0]
            )
        except:
            return None

    # Clean and filter
    for p in products:
        p["numeric_price"] = clean_price(p)

    valid = [p for p in products if p["numeric_price"] is not None]

    # Step 1: Try prioritized sources
    preferred = [p for p in valid if p["Source"] in prioritized_sources]
    if preferred:
        best = min(preferred, key=lambda x: x["numeric_price"])
    else:
        # Step 2: Fallback to eBay or any remaining
        if valid:
            best = min(valid, key=lambda x: x["numeric_price"])
        else:
            return "❌ No valid prices available to make a recommendation."

    return f"✅ Best Buy: {best['Product Name']} at {best['Price']} ({best['Source']})"


def run_scraper_and_get_data(search_query):
    flipkart_data = scrape_flipkart(search_query)
    ebay_data = scrape_ebay(search_query)
    amazon_data = scrape_amazon(search_query)

    # Standardize keys
    flipkart_df = pd.DataFrame(flipkart_data).rename(columns={"Product": "Product Name", "Price": "Price", "Source": "Source"})
    ebay_df = pd.DataFrame(ebay_data).rename(columns={"name": "Product Name", "price": "Price", "source": "Source"})
    amazon_df = pd.DataFrame(amazon_data).rename(columns={"title": "Product Name", "price": "Price", "source": "Source"})

    all_df = pd.concat([flipkart_df, ebay_df, amazon_df], ignore_index=True)
    all_df.to_csv("product_comparison.csv", index=False)

    all_products = all_df.to_dict(orient="records")
    recommendation = recommend_lowest_price(all_products)

    return all_products, recommendation

# Comment this out to prevent auto-running
# if __name__ == "__main__":
#     run_scraper_and_get_data("iphone 16")
