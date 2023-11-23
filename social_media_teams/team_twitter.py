import re
import autogen
from social_media_teams.agents.tweet_agent import TweetAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.utils.tweeter import Tweeter
from analytics_teams.twitter_analytics import TwitterAnalytics
from configs.app_config import AppConfig
import logging
from configs.prompt_config import *

logger = logging.getLogger(__name__)


class TeamTwitter:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()
        logging.info("** PHASE: Twitter Publisher **")

    def post_tweet(self, theme, with_image=False) -> None:
        """
        Create three tweets base on the input data and return them as a list
        """

        # ----------------------------------------
        #          A N A L Y T I C S
        # ----------------------------------------
        # Get insights from the data
        twitter_analytics = TwitterAnalytics()
        data = str(twitter_analytics.twitter_data())  # TODO: Rename the method

        analytics_agent = autogen.AssistantAgent(
            # "analytics_agent",
            twitter_prompts["analytics_agent"]["name"],
            llm_config={
                "config_list": self.config.autogen_config_list,
                "temperature": twitter_prompts["analytics_agent"]["config"]["temperature"],
                "frequency_penalty": twitter_prompts["analytics_agent"]["config"]["frequency_penalty"],
            },
            # system_message=f"You are a analyst. You are tasked with drawing conclusion the this set of data that has been loaded with langchain CSVLoader: {data}. You will then provide some insights and focus points to the tweeter based on this.",
            system_message=twitter_prompts["analytics_agent"]["prompt"].replace("{data}", data)
        )

        user_proxy = autogen.UserProxyAgent(twitter_prompts['analytics_user']['name'], code_execution_config=False)
        user_proxy.initiate_chat(
            analytics_agent,
            # message=f"What conclusions can you draw from this twitter data that has been loaded with langchain CSVLoader: {data} and what focus points can you give the creator of the tweets based on this?",
            message=twitter_prompts["analytics_user"]["prompt"].replace("{data}", data)
        )
        
        # ----------------------------------------
        #          T W E E T I N G
        # ----------------------------------------
        # Tweeter
        tweeter_name = twitter_prompts['tweet_agent']['name']
        tweeter = TweetAgent(
            tweeter_name,
            # f"You are the {tweeter_name}. I want you to a tweet based on this content {self.data} and insights given by the analytics_agent. After each iteration you will wait for the content_reviewer's feedback on the content. The final result should be a string with hashtags at the end. You do not use polite phrases and all answers will be in the requested format, with no other text.",
            twitter_prompts['tweet_agent']['prompt'].replace("{data}", data).replace("{tweeter_name}", tweeter_name),
            self.config.autogen_config_list,
        )
        twitter_agent = tweeter.retrieve_agent()

        # Critic
        criteria_list = str(twitter_prompts['tweet_critic']['criteria_list'])
        critic_name = twitter_prompts['tweet_critic']['name']
        critic = Critic(
            critic_name,
            # f"You are the {critic_name}. You give a rating on from 1 to 5 on the {tweeter_name} suggestions. The rating is based on the following list: {criteria_list}. You will give concrete suggestions if the score is under 5. You should also check that {tweeter_name} sticks to the theme: {theme}. IMPORTANT: make sure the tweet is max 270 characters. You will pause and wait for user feedback after giving 4 / 5 or above. If the output is not in the format of a single string with hashtags at the end, you will ask the tweeter correct it.",
            twitter_prompts['tweet_critic']['prompt']
            .replace("{tweeter_name}", tweeter_name)
            .replace("{criteria_list}", criteria_list)
            .replace("{critic_name}", critic_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name=twitter_prompts['tweet_user']['name'], code_execution_config=False
        )

        group_chat = autogen.GroupChat(
            agents=[analytics_agent, twitter_agent, critic_agent, user_proxy],
            messages=[],
            max_round=10,
        )

        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.config.autogen_config_list},
        )

        # Start prompt
        user_proxy.initiate_chat(
            manager,
            # message=f"write a tweet based on the following theme: {theme} that is somehow related to Gin or to the Gin produces Stookers Gin. The output should be text with hashtags at the end. Do not thank each other for the feedback.",
            message=twitter_prompts['tweet_user']['prompt'].replace("{theme}", theme),
        )

        # ----------------------------------------
        #          L O G S
        # ----------------------------------------
        msg_dic = manager._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                logging.info(f"[{item['name']}]: {item['content']}\n")
            break

        # Get results
        tweet_text = ""
        for v in user_proxy._oai_messages.values():
            tweet_text = v[-2]["content"]

        # ----------------------------------------
        #          I M A G E
        # ----------------------------------------
        if with_image:
            team_image = TeamImage(tweet_text)
            image_path = team_image.create_image("twitter_images")

        # ----------------------------------------
        #          P O S T
        # ----------------------------------------
        tweeter = Tweeter(tweet=tweet_text)  # TODO REMOVE PASSING OF CONFIG
        tweeter.post_tweet()
