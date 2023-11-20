from configs.app_config import AppConfig
from analytics_teams.instagram_analytics import InstagramAnalytics
from social_media_teams.agents.instagram_publisher_agent import InstagramPublisherAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.utils.instagram_publisher import InstagramPublisher
from configs.prompt_config import *
import autogen


class TeamInstagram:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()

    def publish_content(self, theme) -> None:
        instagram_analytics = InstagramAnalytics()
        data = instagram_analytics.instagram_data()

        # ANALYTICS AGENT
        analytics_agent = autogen.AssistantAgent(
            instagram_analytics_agent["name"],
            llm_config={"config_list": self.config.autogen_config_list},
            system_message=instagram_analytics_agent["prompt"].replace(
                "{data}", str(data)
            ),
        )
        user_proxy = autogen.UserProxyAgent(
            instagram_analytics_user["name"], code_execution_config=False
        )
        user_proxy.initiate_chat(
            analytics_agent,
            message=instagram_analytics_user["prompt"].replace("{data}", str(data)),
        )

        # INSTAGRAM PUBLISHER AGENT
        publisher_name = instagram_publisher_agent["name"]
        publisher = InstagramPublisherAgent(
            publisher_name,
            instagram_publisher_agent["prompt"]
            .replace("{instagram_publisher_name}", publisher_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        publisher_agent = publisher.retrieve_agent()

        # CRITIC AGENT
        criteria_list = str(instagram_publisher_critic["criteria_list"])
        critic_name = instagram_publisher_critic["name"]
        critic = Critic(
            critic_name,
            instagram_publisher_critic["prompt"]
            .replace("{critic_name}", critic_name)
            .replace("{criteria_list}", criteria_list)
            .replace("{instagram_publisher_name}", publisher_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy", code_execution_config=False
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
        user_proxy.initiate_chat(
            manager,
            message=instagram_publisher_user["prompt"].replace("{theme}", theme),
            # message=f"write an Instagram caption based on the following theme: {theme} that is somehow related to Gin or to the Gin produces Stookers Gin. The output should be text with hashtags at the end. I want the hashtags: #Stookers #Amsterdam to always be present. Do not thank each other for the feedback.",
        )

        instagram_caption = ""
        for v in user_proxy._oai_messages.values():
            instagram_caption = v[-2]["content"]

        team_image = TeamImage(instagram_caption)
        filename = team_image.create_image("instagram_images")

        publisher = InstagramPublisher()
        publisher.publish(filename, instagram_caption)
