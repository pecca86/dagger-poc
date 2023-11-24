import autogen
from utils.file_utils import save_to_csv
from enums.platform import Platform
import requests
from configs.app_config import AppConfig
# from langchain.document_loaders.csv_loader import CSVLoader
import shutil
import os


# TODO: Make a more refined method to retrieve the data from the CSV file
# TODO: Check if we can use pandas for some parts of the analytics
class InstagramAnalytics:
    def __init__(self) -> None:
        self.config = AppConfig()

    def collect_data(self):
        media_ids = self._all_published_media()
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

    def _all_published_media(self) -> list:
        #TODO: Check if the media_id has been queried in the past 2 days, if so, don't query it again
        """
        Call Instagram endpoint to retrieve all media ids that are published
        """
        url = f"https://graph.facebook.com/v18.0/{self.config.meta_instagram_app_id}/media"
        headers = {
            "Authorization": f"Bearer {self.config.instagram_long_term_access_token}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        image_data = data["data"]
        image_ids = []
        for entry in image_data:
            image_ids.append(entry["id"])
        print(image_ids)

        return image_ids

    def _media_info(self, media_ids: list) -> list[dict]:
        """
        Call Instagram endpoint to retrieve media info from id specified in the list
        Structure: [{'id': '1', 'caption': 'string', 'comments_count': 9, 'like_count': 10, 'media_product_type': 'string', 'media_type': 'string', 'timestamp': 'string'}]
        """
        media_info = []
        for id in media_ids:
            url = f"https://graph.facebook.com/v18.0/{id}?fields=caption,comments_count,like_count,media_product_type,media_type,timestamp&access_token={self.config.instagram_long_term_access_token}"
            response = requests.get(url)
            data = response.json()
            print(data)
            media_info.append(data)
        
        return media_info

    def top_posts(self):
        return self.__retrieve_post_data()

    def __retrieve_post_data(self):
        """
        Call the instagram API to retrieve the data based on the CSV of posts.
        After this save the data to a CSV file for further analytics that can be passed on to the researcher.
        """

        return [
            "Curious to know what the best gin is? Check out our website! #Stookers #Gin #Amsterdam",
            "Gin is the best drink ever! Especially when you drink it with your friends! #luvthattaste #ginislife",
            "I just looooove this recepie! 20cl of gin, some ice, and a slice of lemon! #gin #ginlovers #ginislife",
        ]

    # def instagram_data(self):
    #     loader = CSVLoader(
    #         file_path="./analytics_data/ig_posts_data.csv",
    #         csv_args={
    #             "delimiter": "|",
    #             "quotechar": '"',
    #             "fieldnames": [
    #                 "media_id",
    #                 "caption",
    #                 "comments_count",
    #                 "like_count",
    #                 "media_product_type",
    #                 "media_type",
    #                 "timestamp",
    #             ],
    #         },
    #     )

    #     data = loader.load()
    #     return data
