import requests
from configs.app_config import AppConfig
from enums.platform import Platform
from utils.file_utils import save_to_csv
import shutil
import os
config = AppConfig()

class InstagramApiTeam:
    def __self__(self):
        pass

    """
    Collect media data to CSV
    """
    def collect_data(self):
        media_ids = self.all_media_ids()
        media_info = self._media_info(media_ids)
        csv_headers = [
            "media_id",
            "caption",
            "comments_count",
            "like_count",
            "media_product_type",
            "media_type",
            "timestamp",
        ]
        #delete existing file if exists using shutil
        if os.path.exists(os.path.join(os.getcwd(), "analytics_data", "ig_posts_data.csv")):
            os.remove(os.path.join(os.getcwd(), "analytics_data", "ig_posts_data.csv"))
            
        save_to_csv(
            file_name="ig_posts_data.csv",
            headers=csv_headers,
            data=media_info,
            platform=Platform.INSTAGRAM,
        )

    """
    GET all media ids
    """
    def all_media_ids(self):
        url = f"https://graph.facebook.com/v18.0/{config.meta_instagram_app_id}/media"
        headers = {
            "Authorization": f"Bearer {config.instagram_long_term_access_token}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        image_data = data["data"]
        image_ids = []
        for entry in image_data:
            image_ids.append(entry["id"])
        return image_ids
    
    """
    GET Media data by media id
    """
    def _media_info(self, media_ids: list) -> list[dict]:
        """
        Call Instagram endpoint to retrieve media info from id specified in the list
        Structure: [{'id': '1', 'caption': 'string', 'comments_count': 9, 'like_count': 10, 'media_product_type': 'string', 'media_type': 'string', 'timestamp': 'string'}]
        """
        media_info = []
        for id in media_ids:
            url = f"https://graph.facebook.com/v18.0/{id}?fields=caption,comments_count,like_count,media_product_type,media_type,timestamp&access_token={config.instagram_long_term_access_token}"
            response = requests.get(url)
            data = response.json()
            media_info.append(data)
        
        return media_info

    """
    GET comment data by media id
    """
    # 18017013670932825
    def all_comments_from_media(self, media_id:str) -> list[object]:
        url = f"https://graph.facebook.com/v18.0/{media_id}?fields=comments&access_token={config.instagram_long_term_access_token}"
        response = requests.get(url)
        # { comments: { data: [ { timestamp: 12132, text: blablabla, id: 23213213} ] } }
        comments = response.json()['comments']['data']

        return comments


    """
    GET comment info by comment id
    """
    # 18107939269347722
    def comment_info(self, comment_id:str) -> object:
        url = f"https://graph.facebook.com/v18.0/{comment_id}?fields=from,id&access_token={config.instagram_long_term_access_token}"
        response = requests.get(url)
        return response.json()


    """
    POST reply to commeny by id
    """
    # 18107939269347722
    def reply_to_comment(self, comment_id:str, message:str) -> str:
        url = f"https://graph.facebook.com/v18.0/{comment_id}/replies?message={message}&access_token={config.instagram_long_term_access_token}"
        response = requests.post(url)
        return response.json()['id']