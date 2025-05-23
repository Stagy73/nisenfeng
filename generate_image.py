# generate_image.py
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def generate_pinterest_image(product, output_path="output/pin.png"):
    response = requests.get(product["image"])
    img = Image.open(BytesIO(response.content)).convert("RGB").resize((1000, 1500))

    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("arial.ttf", 40)
    font_price = ImageFont.truetype("arial.ttf", 50)

    draw.text((50, 1300), product["title"][:40], fill="white", font=font_title)
    draw.text((50, 1400), f"{product['price']}", fill="yellow", font=font_price)

    img.save(output_path)
