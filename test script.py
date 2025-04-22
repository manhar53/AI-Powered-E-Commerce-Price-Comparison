from scrape_amazon import scrape_amazon

search_query = "iPhone 15"

amazon_data = scrape_amazon(search_query)

print("🔍 Amazon Results:")
for product in amazon_data:
    print(f"✔ {product['Product']} - {product['Price']} ({product['Source']})")
