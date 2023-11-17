from requests_oauthlib import OAuth1Session
import os
import json
from decouple import config
from utils.file_utils import save_to_csv
import time
import re
from configs.app_config import AppConfig
from enums.platform import Platform


# TODO: Check how to upload media (If available under free plan...)
class Tweeter:
    def __init__(self, tweet):
        self.tweet = tweet
        self.config = AppConfig()

    def save_tweet_data(self, tweet_data: json, with_image_data=False):
        """
        Save tweet data to a file to be used for analytics
        """
        #TODO: On media flow, save the media_id as well1
        print("ID: ", tweet_data['data']['id'])
        timestamp = str(int(time.time()))
        save_to_csv(
            "own_tweets.csv",
            ["tweet_id", "tweet_text", "timestamp"],
            [tweet_data["data"]["id"], tweet_data["data"]["text"], timestamp],
            Platform.TWITTER,
        )

    #TODO: Create a flow for uploading images
    # This requires a different endpoint for first uploading the image, then using the media_id for the tweet
    def post_tweet(self, image=None) -> json:
        payload = {"text": self.tweet}
        print("Payload: ", payload['text'])
        
        cleaned_payload = re.sub('^"|"$', '', payload['text']) #cleans the double quotes from the tweet
        payload['text'] = cleaned_payload

        # Get request token
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(self.config.twitter_consumer_key, client_secret=self.config.twitter_consumer_secret)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.config.twitter_consumer_key,
            client_secret=self.config.twitter_consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Make the request
        oauth = OAuth1Session(
            self.config.twitter_consumer_key,
            client_secret=self.config.twitter_consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        self.save_tweet_data(json_response, with_image_data=False)

        return json_response
