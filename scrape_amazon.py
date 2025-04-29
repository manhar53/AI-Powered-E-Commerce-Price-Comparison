import requests

def scrape_amazon(search_query):
    api_key = ""
    url = "https://api.rainforestapi.com/request"
    
    params = {
        "api_key": api_key,
        "type": "search",
        "amazon_domain": "amazon.in",
        "search_term": search_query
    }

    response = requests.get(url, params=params)
    results = response.json()

    products = []
    for item in results.get("search_results", [])[:15]:  # Limit to first 15 products
        name = item.get("title")
        price = item.get("price", {}).get("raw", "N/A")
        image = item.get("image")
        if name:
            products.append({
                "name": name,
                "price": price,
                "source": "Amazon",
                "url": item.get("link"),
                "Image": image
            })

    return products
