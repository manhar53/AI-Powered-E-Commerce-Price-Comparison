import requests
from bs4 import BeautifulSoup

def scrape_flipkart(search_query):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = []
    for item in soup.find_all("div", class_="KzDlHZ"):
        try:
            # Get image
            image = None
            img_tag = item.find("img")
            if img_tag:
                image = img_tag.get("src") or img_tag.get("data-src")

            
            # Get product name
            name = item.text.strip()
            
            # Get price
            price = item.find_next("div", class_="Nx9bqj _4b5DiR").text.strip()

            # Get product URL
            a_tag = item.find_parent("a", href=True)
            product_url = "https://www.flipkart.com" + a_tag["href"] if a_tag else None
            
            # Append product data
            products.append({
                "Product": name,
                "Price": price,
                "Source": "Flipkart",
                "url": product_url,
                "Image": image
            })
        except Exception as e:
            continue
    
    return products
