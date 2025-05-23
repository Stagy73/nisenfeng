# post_to_pinterest.py
import requests

def post_to_pinterest(image_path, title, link, board_id, access_token):
    url = "https://api.pinterest.com/v5/pins"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    json_data = {
        "board_id": board_id,
        "title": title,
        "alt_text": title,
        "media_source": {
            "source_type": "image_base64",
            "content_type": "image/jpeg",
            "data": open(image_path, "rb").read().encode("base64").decode()
        },
        "link": link
    }

    response = requests.post(url, headers=headers, json=json_data)
    return response.status_code, response.text
