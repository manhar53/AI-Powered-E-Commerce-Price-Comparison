import requests
from bs4 import BeautifulSoup

def scrape_ebay(search_query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []
    conversion_rate = 83  # USD to INR

    for item in soup.select(".s-item"):
        if len(products) >= 15:
            break

        name_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        link_tag = item.select_one("a.s-item__link")
        img_tag = item.select_one(".s-item__image-img")

        if name_tag and price_tag and "Shop on eBay" not in name_tag.text:
            name = name_tag.text.strip()
            price_usd = price_tag.text.strip().replace("$", "").split()[0].replace(",", "")

            try:
                price_inr = round(float(price_usd) * conversion_rate)
                formatted_price = f"₹{price_inr}"
            except:
                formatted_price = "N/A"

            product_url = link_tag["href"] if link_tag else None
            image = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

            products.append({
                "name": name,
                "price": formatted_price,
                "source": "eBay",
                "url": product_url,
                "Image": image
            })

    return products
