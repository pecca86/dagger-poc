from decouple import config
import autogen


# class AppConfig:
#     def __init__(self):
#         # Config for autogen
#         self.autogen_model = config("AUTOGEN_MODEL")
#         self.autogen_config_list = [
#             {
#                 "model": config("AUTOGEN_MODEL"),
#                 "api_key": config("OPENAI_API_KEY"),
#             }
#         ]
#         # Open AI
#         self.openai_api_key = config('OPENAI_API_KEY')
#         # Twitter
#         self.twitter_consumer_key = config('TWITTER_CONSUMER_KEY')
#         self.twitter_consumer_secret = config('TWITTER_CONSUMER_SECRET')
#         self.twitter_access_token = config('TWITTER_ACCESS_TOKEN')
#         self.twitter_access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')
#         self.twitter_bearer_token = config('TWITTER_BEARER_TOKEN')
#         self.twitter_oauth2_client_id = config('TWITTER_OAUTH2_CLIENT_ID')
#         self.twitter_oauth2_client_secret = config('TWITTER_OAUTH2_CLIENT_SECRET')
#         self.twitter_with_image = config('TWITTER_WITH_IMAGE')
#         #Instagram
#         self.instagram_long_term_access_token = config('INSTAGRAM_LONG_TERM_ACCESS_TOKEN')
#         self.meta_instagram_app_id = config("META_INSTAGRAM_APP_ID")

class AppConfig:
    def __init__(self):
        self.app_name = "Gin Media Team"
        self.app_version = "1.0.0"
        # Config for autogen
        self.autogen_model = config("AUTOGEN_MODEL")
        self.autogen_config_list = [
            {
                "model": config("AUTOGEN_MODEL"),
                "api_key": config("OPENAI_API_KEY"),
            }
        ]
        # Open AI
        self.openai_api_key = config('OPENAI_API_KEY')
        # Twitter
        self.twitter_consumer_key = config('TWITTER_CONSUMER_KEY')
        self.twitter_consumer_secret = config('TWITTER_CONSUMER_SECRET')
        self.twitter_access_token = config('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')
        self.twitter_bearer_token = config('TWITTER_BEARER_TOKEN')
        self.twitter_oauth2_client_id = config('TWITTER_OAUTH2_CLIENT_ID')
        self.twitter_oauth2_client_secret = config('TWITTER_OAUTH2_CLIENT_SECRET')
        self.twitter_with_image = config('TWITTER_WITH_IMAGE')
        #Instagram
        self.instagram_long_term_access_token = config('INSTAGRAM_LONG_TERM_ACCESS_TOKEN')
        self.meta_instagram_app_id = config("META_INSTAGRAM_APP_ID")