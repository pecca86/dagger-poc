"""
Call Instagram endpoint to retrieve all media ids that are published
"""
import requests
from configs.app_config import AppConfig
config = AppConfig()

url = f"https://graph.facebook.com/v18.0/{config.meta_instagram_app_id}/media"
headers = {
    "Authorization": f"Bearer {config.instagram_long_term_access_token}"
}
response = requests.get(url, headers=headers)
data = response.json()
print(data)
image_data = data["data"]
image_ids = []
for entry in image_data:
    image_ids.append(entry["id"])
print(image_ids)

"""
Get Info by media id
"""

"""
Get insights by media id
"""

"""
Get insights by account id
"""