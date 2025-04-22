from scrape_flipkart import scrape_flipkart
from scrape_ebay import scrape_ebay
from scrape_amazon import scrape_amazon  # Make sure this file and function exist

search_query = "iPhone 14"

# Flipkart
flipkart_data = scrape_flipkart(search_query)
print("🔍 Flipkart Results:")
for product in flipkart_data:
    print(f"✔ {product['Product']} - {product['Price']} ({product['Source']})")

# eBay
ebay_data = scrape_ebay(search_query)
print("\n🔍 eBay Results:")
for product in ebay_data:
    print(f"✔ {product['name']} - {product['price']} ({product['source']})")

# Amazon (Rainforest API)
amazon_data = scrape_amazon(search_query)
print("\n🔍 Amazon Results:")
for product in amazon_data:
    try:
        print(f"✔ {product['name']} - {product['price']} ({product['source']})")
    except KeyError:
        print("❌ Invalid product format:", product)
