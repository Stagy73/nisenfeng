# search_amazon.py
def search_products_manual():
    print("Entrez les informations du produit Amazon :")
    title = input("Titre du produit : ")
    price = input("Prix (ex: 19,99 €) : ")
    image_url = input("URL de l'image : ")
    affiliate_link = input("Lien affilié complet (avec nisenfeng-21) : ")

    return [{
        "title": title,
        "price": price,
        "image": image_url,
        "url": affiliate_link
    }]
