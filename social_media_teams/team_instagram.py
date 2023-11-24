from configs.app_config import AppConfig
from analytics_teams.instagram_analytics import InstagramAnalytics
from social_media_teams.agents.instagram_publisher_agent import InstagramPublisherAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.utils.instagram_publisher import InstagramPublisher
from configs.prompt_config import *
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import autogen
import logging
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)


class TeamInstagram:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()

    def publish_content(self, theme) -> None:
        # instagram_analytics = InstagramAnalytics()
        # data = instagram_analytics.instagram_data()

        # ----------------------------------------
        #          A N A L Y T I C S
        # ----------------------------------------
        # ANALYTICS AGENT
        # analytics_agent = autogen.AssistantAgent(
        #     instagram_prompts["analytics_agent"]["name"],
        #     llm_config={
        #         "config_list": self.config.autogen_config_list,
        #         "temperature": instagram_prompts["analytics_agent"]["config"][
        #             "temperature"
        #         ],
        #         "frequency_penalty": instagram_prompts["analytics_agent"]["config"][
        #             "frequency_penalty"
        #         ],
        #     },
        #     system_message=instagram_prompts["analytics_agent"]["prompt"].replace(
        #         "{data}", str(data)
        #     ),
        # )
        # # User proxy
        # user_proxy = autogen.UserProxyAgent(
        #     instagram_prompts["analytics_user"]["name"], code_execution_config=False
        # )

        # # Start prompt
        # user_proxy.initiate_chat(
        #     analytics_agent,
        #     message=instagram_prompts["analytics_user"]["prompt"].replace(
        #         "{data}", str(data)
        #     ),
        # )

        # ----------------------------------------
        #          C R E A T E  C O N T E N T  W I T H  A N A L Y T I C S
        # ----------------------------------------

        # ANALYTICS AGENT
        analytics_agent = autogen.AssistantAgent(
            name="analyst",
            system_message="You are a data analyst specialized in analyzing trends in instagram data, given to you by the raqproxy agent. You will reiterate according to feedback given by the critic.",
            llm_config=self.config.autogen_config_list,
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
                "docs_path": "./analytics_data/ig_posts_data.csv",
                "embedding_function": openai_ef,
            },
        )

        # INSTAGRAM PUBLISHER AGENT
        publisher_name = instagram_prompts["publisher_agent"]["name"]
        publisher = InstagramPublisherAgent(
            publisher_name,
            # instagram_publisher_agent["prompt"]
            instagram_prompts["publisher_agent"]["prompt"]
            .replace("{instagram_publisher_name}", publisher_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        publisher_agent = publisher.retrieve_agent()

        # CRITIC AGENT
        criteria_list = str(instagram_prompts["publisher_critic"]["criteria_list"])
        critic_name = instagram_prompts["publisher_critic"]["name"]
        critic = Critic(
            critic_name,
            instagram_prompts["publisher_critic"]["prompt"]
            .replace("{critic_name}", critic_name)
            .replace("{criteria_list}", criteria_list)
            .replace("{instagram_publisher_name}", publisher_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy", 
            code_execution_config=False
        )

        group_chat = autogen.GroupChat(
            agents=[analytics_agent, publisher_agent, critic_agent, user_proxy],
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
            problem=instagram_prompts["publisher_user"]["prompt"].replace(
                "{theme}", theme
            ),
        )

        # ----------------------------------------
        #          L O G S
        # ----------------------------------------
        msg_dic = manager._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                logging.info(f"[{item['name']}]: {item['content']}\n")
            break

        instagram_caption = ""
        for v in user_proxy._oai_messages.values():
            instagram_caption = v[-2]["content"]

        # ----------------------------------------
        #          L O G S
        # ----------------------------------------
        team_image = TeamImage(instagram_caption)
        filename = team_image.create_image("instagram_images")

        # ----------------------------------------
        #          P U B L I S H
        # ----------------------------------------
        publisher = InstagramPublisher()
        publisher.publish(filename, instagram_caption)
