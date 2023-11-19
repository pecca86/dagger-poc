import re
import autogen
from social_media_teams.agents.tweet_agent import TweetAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.utils.tweeter import Tweeter
from analytics_teams.twitter_analytics import TwitterAnalytics
from configs.app_config import AppConfig


class TeamTwitter:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()

    def post_tweet(self, theme, with_image=False) -> None:
        """
        Create three tweets base on the input data and return them as a list
        """

        # Get insights from the data
        twitter_analytics = TwitterAnalytics()
        data = twitter_analytics.twitter_data() #TODO: Rename the method

        # TODO: Create a Analytics agent or not?
        analytics_agent = autogen.AssistantAgent("analytics_agent", llm_config={"config_list": self.config.autogen_config_list}, system_message=f"You are a analyst. You are tasked with drawing conclusion the this set of data that has been loaded with langchain CSVLoader: {data}. You will then provide some insights and focus points to the tweeter based on this.")
        user_proxy = autogen.UserProxyAgent("user_proxy", code_execution_config=False)
        user_proxy.initiate_chat(analytics_agent, message=f"What conclusions can you draw from this twitter data that has been loaded with langchain CSVLoader: {data} and what focus points can you give the creator of the tweets based on this? ")

        # Tweeter
        tweeter_name = "tweeter"
        tweeter = TweetAgent(
            tweeter_name,
            f"You are the {tweeter_name}. I want you to a tweet based on this content {self.data} and insights given by the analytics_agent. After each iteration you will wait for the content_reviewer's feedback on the content. The final result should be a string with hashtags at the end. You do not use polite phrases and all answers will be in the requested format, with no other text.",
            self.config.autogen_config_list,
        )
        twitter_agent = tweeter.retrieve_agent()

        # Critic
        criteria_list = [
            "Is there max 280 characters in the tweet? Emojis count as 2 characters.",
            "Is the text relevant to the topic?",
            "Is the text grammatically correct?",
            "Is the text concise?",
            "Is the text twitter friendly?",
            "Did the tweet take into consideration the analytics_agent's insights?",
        ]
        critic_name = "critic"
        critic = Critic(
            critic_name,
            f"You are the {critic_name}. You give a rating on from 1 to 5 on the {tweeter_name} suggestions. The rating is based on the following list: {criteria_list}. You will give concrete suggestions if the score is under 5. You should also check that {tweeter_name} sticks to the theme: {theme}. IMPORTANT: make sure the tweet is max 270 characters. You will pause and wait for user feedback after giving 4 / 5 or above. If the output is not in the format of a single string with hashtags at the end, you will ask the tweeter correct it.",
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy", code_execution_config=False
        )

        group_chat = autogen.GroupChat(
            agents=[analytics_agent, twitter_agent, critic_agent, user_proxy], messages=[], max_round=10
        )

        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.config.autogen_config_list},
        )

        # Start prompt
        user_proxy.initiate_chat(
            manager,
            message=f"write a tweet based on the following theme: {theme} that is somehow related to Gin or to the Gin produces Stookers Gin. The output should be text with hashtags at the end. Do not thank each other for the feedback.",
        )

        tweet_text = ""
        for v in user_proxy._oai_messages.values():
            # tweet_text = v[-2]["content"]
            tweet_text = v[-2]["content"]

        if with_image:
            team_image = TeamImage(tweet_text)
            image_path = team_image.create_image("twitter_images")

        tweeter = Tweeter(tweet=tweet_text) # TODO REMOVE PASSING OF CONFIG
        tweeter.post_tweet()
