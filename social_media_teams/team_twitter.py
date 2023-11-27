import re
import autogen
from social_media_teams.agents.tweet_agent import TweetAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.utils.tweeter import Tweeter
from social_media_teams.utils.tweeter_v2 import TweeterV2
from analytics_teams.twitter_analytics import TwitterAnalytics
from social_media_teams.agents.marketing_agent import MarketingAgent
from configs.app_config import AppConfig
import logging
import random
from configs.prompt_config import *
from chromadb.utils import embedding_functions
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent


logger = logging.getLogger(__name__)


class TeamTwitter:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()
        logging.info("** PHASE: Twitter Team **")

    # ----------------------------------------
    #          T W E E T  M A R K E T I N G
    # ----------------------------------------
    def tweet_marketing(self):
        logging.info("** PHASE: Twitter Team - Marketing **")

        marketing_agent_name = instagram_prompts["marketing_agent"]["name"]
        marketing_agent = MarketingAgent(
            marketing_agent_name,
            system_message=instagram_prompts["marketing_agent"]["prompt"],
            agent_config=self.config.autogen_config_list,
        )
        marketing_agent_agent = marketing_agent.retrieve_agent()

        user_proxy = autogen.UserProxyAgent(
            name="marketing_user",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

        user_proxy.initiate_chat(
            marketing_agent_agent,
            message=instagram_prompts["marketing_user"]["prompt"],
        )

        tweet_text = ""
        for v in user_proxy._oai_messages.values():
            tweet_text = v[-1]["content"]

        # LOGGING
        msg_dic = user_proxy._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                logging.info(f"[{item['role']}]: {item['content']}\n")
            break

        tweeter_v2 = TweeterV2(tweet=tweet_text)

        random_number = random.randint(0, 9)
        image_url = f"https://cdn.shopify.com/s/files/1/0522/7357/8152/files/instagram{random_number}.jpg"
        tweeter_v2.tweet_with_image(image_url)

    # ----------------------------------------
    #          T W E E T  F U N  F A C T
    # ----------------------------------------
    def tweet_fun_fact(self, theme, with_image=False) -> None:
        logging.info("** PHASE: Twitter Team - Fun Fact **")

        # ANALYTICS AGENT
        analytics_agent = autogen.AssistantAgent(
            name="analyst",
            system_message="You are a data analyst specialized in analyzing trends in twitter data, given to you by the raqproxy agent. You will reiterate according to feedback given by the critic.",
            llm_config={
                "config_list": self.config.autogen_config_list,
                "temperature": 0,
                "frequency_penalty": 0,
                "timeout": 120,
            },
        )

        # RAG USER PROXY AGENT
        # Embedding function
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=self.config.openai_api_key,
            model_name="text-embedding-ada-002",
        )

        ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            system_message="You are the ragproxyagent. You will retrieve content for the analyst to analyze.",
            human_input_mode="NEVER",
            retrieve_config={
                "task": "qa",
                "docs_path": "./analytics_data/twitter.csv",
                "embedding_function": openai_ef,
            },
        )

        # Tweeter
        tweeter_name = twitter_prompts["tweet_agent"]["name"]
        tweeter = TweetAgent(
            tweeter_name,
            twitter_prompts["tweet_agent"]["prompt"]
            .replace("{data}", self.data)
            .replace("{tweeter_name}", tweeter_name),
            self.config.autogen_config_list,
        )
        twitter_agent = tweeter.retrieve_agent()

        # Critic
        criteria_list = str(twitter_prompts["tweet_critic"]["criteria_list"])
        critic_name = twitter_prompts["tweet_critic"]["name"]
        critic = Critic(
            critic_name,
            twitter_prompts["tweet_critic"]["prompt"]
            .replace("{tweeter_name}", tweeter_name)
            .replace("{criteria_list}", criteria_list)
            .replace("{critic_name}", critic_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name=twitter_prompts["tweet_user"]["name"], code_execution_config=False
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
        ragproxyagent.initiate_chat(
            manager,
            problem=twitter_prompts["tweet_user"]["prompt"].replace("{theme}", theme),
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
        tweeter_v2 = TweeterV2(tweet=tweet_text)
        tweeter_v2.post_tweet()
