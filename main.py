from search_amazon import search_products_manual as search_products
from generate_image import generate_pinterest_image
from post_to_pinterest import post_to_pinterest
import os

# Crée le dossier de sortie s'il n'existe pas
if not os.path.exists("output"):
    os.makedirs("output")

# L'utilisateur entre les infos produit manuellement
products = search_products()

# Paramètres Pinterest à personnaliser
access_token = "VOTRE_TOKEN_PINTEREST"
board_id = "VOTRE_BOARD_ID"

# Pour chaque produit entré
for i, product in enumerate(products):
    print(f"{i+1}. {product['title']} - {product['price']}")
    image_path = f"output/pin_{i}.png"

    # Génération de l’image
    generate_pinterest_image(product, output_path=image_path)
    print(f"Image créée : {image_path}\nLien affilié : {product['url']}")

    # Publication Pinterest
    status, response = post_to_pinterest(
        image_path,
        product['title'],
        product['url'],
        board_id,
        access_token
    )

    print(f"Pinterest Status: {status}\n{response}\n")
