"""
Call Instagram endpoint to retrieve all media ids that are published
"""
import requests
from configs.app_config import AppConfig
config = AppConfig()

"""
GET all media ids
"""
def all_media_ids():
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
GET Info by media id
"""
# 18017013670932825
def all_comment_from_media(media_id:str):
    access_token = config.instagram_long_term_access_token
    url = f"https://graph.facebook.com/v18.0/{media_id}?fields=comments&access_token={access_token}"
    response = requests.get(url)
    # { comments: { data: [ { timestamp: 12132, text: blablabla, id: 23213213} ] } }
    comments = response.json()['comments']['data']
    for comment in comments:
        print(comment['text'])
        print(comment['id'])

"""
GET comment info by comment id
"""
# 18107939269347722
def comment_info(comment_id:str):
    access_token = config.instagram_long_term_access_token
    url = f"https://graph.facebook.com/v18.0/{comment_id}?fields=from,id&access_token={access_token}"
    response = requests.get(url)
    print(response.json())
    print(response)['from']['id']
    print(response)['from']['username']

"""
POST reply to commeny by id
"""
# 18107939269347722
def reply_to_comment(comment_id:str, message:str):
    access_token = config.instagram_long_term_access_token
    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies?message={message}&access_token={access_token}"
    response = requests.post(url)
    print(response.json())

"""
GET insights by media id
"""

"""
GET insights by account id
"""

reply_to_comment('18107939269347722', '@pexi86 your ingredients will be featured in our next post!')
