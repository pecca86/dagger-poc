"""
NOTE! We meed to have Twurl installed on our host machine in order for this code to work.
"""
import os
import subprocess
import json
import logging
from utils.file_utils import save_to_csv, download_file
from enums.platform import Platform
import time
import re
from configs.app_config import AppConfig


class TweeterV2:
    config = AppConfig()

    def __init__(self, tweet: str):
        self.tweet = tweet

    def post_tweet(self) -> json:
        cleaned_text = re.sub(
            '^"|"$', "", self.tweet
        )  # cleans the double quotes from the tweet

        print("Tweeting: ", cleaned_text)

        tweet_with_text_cmd = (
            'twurl -A "Content-Type: application/json" -X POST "/2/tweets" -d \'{"text": "'
            + cleaned_text
            + "\"}'"
        )

        proc = subprocess.run(tweet_with_text_cmd, shell=True, capture_output=True)
        json_response = proc.stdout.decode("utf-8").replace("'", '"')
        response = json.loads(json_response)

        print(response)
        logging.info("Tweet successfully posted.")

        self.save_tweet_data(response, with_image_data=False)

        return response

    def tweet_with_image(self, image_url):
        cleaned_text = re.sub(
            '^"|"$', "", self.tweet
        )  # cleans the double quotes from the tweet

        media_id = self._upload_image(image_url)
        payload = {"text": cleaned_text, "media": {"media_ids": [media_id]}}
        tweet_payload = json.dumps(payload, ensure_ascii=True) #str(payload).replace("'", '"')
        tweet_payload = tweet_payload.replace("'", '`')

        # cmd = "twurl -A \"Content-Type: application/json\" -X POST \"/2/tweets\" -d '{\"text\": " + self.tweet + ", \"media\": {\"media_ids\": [\"" + media_id + "\"]}}'"
        cmd = f"twurl -A \"Content-Type: application/json\" -X POST \"/2/tweets\" -d '{tweet_payload}'"

        proc = subprocess.run(cmd, shell=True, capture_output=True)
        json_response = proc.stdout.decode("utf-8").replace("'", '"')
        response = json.loads(json_response)
        self.save_tweet_data(response, with_image_data=False)

    def _upload_image(self, image_url) -> str:
        download_file(image_url, "./twitter_images/twitter_temp.jpg")
        upload_cmd = 'twurl -H "upload.twitter.com" -X POST "/1.1/media/upload.json" --file "./twitter_images/twitter_temp.jpg" --file-field "media"'
        proc = subprocess.run(upload_cmd, shell=True, capture_output=True)
        json_text = proc.stdout.decode("utf-8").replace("'", '"')
        response = json.loads(json_text)
        media_id = response["media_id_string"]
        return media_id

    def save_tweet_data(self, tweet_data: json, with_image_data=False):
        """
        Save tweet data to a file to be used for analytics
        """
        # TODO: On media flow, save the media_id as well1
        print("ID: ", tweet_data["data"]["id"])
        timestamp = str(int(time.time()))
        save_to_csv(
            "own_tweets.csv",
            ["tweet_id", "tweet_text", "timestamp"],
            [tweet_data["data"]["id"], tweet_data["data"]["text"], timestamp],
            Platform.TWITTER,
        )
