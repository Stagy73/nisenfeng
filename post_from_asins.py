import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

AFFILIATE_TAG = "nisenfeng-21"
ACCESS_TOKEN = "VOTRE_TOKEN_PINTEREST"
BOARD_ID = "VOTRE_BOARD_ID"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    )
}

def fetch_amazon_data(asin):
    url = f"https://www.amazon.fr/dp/{asin}/?tag={AFFILIATE_TAG}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        title_tag = soup.find(id="productTitle")
        title = title_tag.get_text(strip=True) if title_tag else "Titre non trouvé"

        image_tag = soup.find("img", {"id": "landingImage"})
        image_url = image_tag["src"] if image_tag else None

        price_whole = soup.find("span", {"class": "a-price-whole"})
        price_fraction = soup.find("span", {"class": "a-price-fraction"})
        if price_whole and price_fraction:
            price = f"{price_whole.text.strip()},{price_fraction.text.strip()} €"
        else:
            price = "Prix non trouvé"

        return {
            "title": title,
            "price": price,
            "image_url": image_url,
            "affiliate_url": url
        }
    except Exception as e:
        print(f"Erreur avec ASIN {asin}: {e}")
        return None

def create_image(title, price, image_url, output_path):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGB").resize((1000, 1500))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_price = ImageFont.truetype("arial.ttf", 50)
    except:
        font_title = font_price = ImageFont.load_default()

    draw.text((50, 1300), title[:60], fill="white", font=font_title)
    draw.text((50, 1400), price, fill="yellow", font=font_price)
    img.save(output_path)

def post_to_pinterest(image_path, title, link):
    url = "https://api.pinterest.com/v5/pins"
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    import base64
    encoded_image = base64.b64encode(image_data).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    json_data = {
        "board_id": BOARD_ID,
        "title": title,
        "alt_text": title,
        "media_source": {
            "source_type": "image_base64",
            "content_type": "image/jpeg",
            "data": encoded_image
        },
        "link": link
    }

    response = requests.post(url, headers=headers, json=json_data)
    print(f"Pinterest Status: {response.status_code}")
    print(response.text)

def main():
    if not os.path.exists("output"):
        os.makedirs("output")

    with open("asins.txt", "r") as f:
        asins = [line.strip() for line in f if line.strip()]

    for i, asin in enumerate(asins):
        print(f"Traitement de l'ASIN {asin}...")
        data = fetch_amazon_data(asin)
        if not data or not data.get("image_url"):
            print(f"Erreur ou image introuvable pour {asin}")
            continue

        image_path = f"output/product_{i}.jpg"
        create_image(data['title'], data['price'], data['image_url'], image_path)
        post_to_pinterest(image_path, data['title'], data['affiliate_url'])

if __name__ == "__main__":
    main()
