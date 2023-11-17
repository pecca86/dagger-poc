from configs.app_config import AppConfig
from analytics_teams.instagram_analytics import InstagramAnalytics
from social_media_teams.agents.instagram_publisher_agent import InstagramPublisherAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.utils.instagram_publisher import InstagramPublisher
import autogen

class TeamInstagram:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()

    def publish_content(self, theme) -> None:
        instagram_analytics = InstagramAnalytics()
        data = instagram_analytics.instagram_data()

        # ANALYTICS AGENT
        analytics_agent = autogen.AssistantAgent("analytics_agent", llm_config={"config_list": self.config.autogen_config_list}, system_message=f"You are a analyst. You are tasked with drawing conclusion the this set of data that has been loaded with langchain CSVLoader: {data}. You will then provide some insights and focus points to the instagram_publisher based on this.")
        user_proxy = autogen.UserProxyAgent("user_proxy", code_execution_config=False)
        user_proxy.initiate_chat(analytics_agent, message=f"What conclusions can you draw from this instagram data that has been loaded with langchain CSVLoader: {data} and what focus points can you give the instagram_publisher based on this? ")

        # INSTAGRAM PUBLISHER AGENT
        instagram_publisher_name = "instagram_publisher"
        instagram_publisher = InstagramPublisherAgent(
            instagram_publisher_name,
            f"You are the {instagram_publisher_name}. I want you to a tweet based on this content {self.data} and insights given by the analytics_agent. After each iteration you will wait for the content_reviewer's feedback on the content. The final result should be a short instagram caption with hashtags at the end. You do not use polite phrases and all answers will be in the requested format, with no other text.",
            self.config.autogen_config_list,
        )
        instagram_publisher_agent = instagram_publisher.retrieve_agent()

        # CRITIC AGENT
        criteria_list = [
            "Is the text instagram friendly?",
            "Is the text relevant to the topic?",
            "Is the text grammatically correct?",
            "Is the text concise?",
            "Did the tweet take into consideration the analytics_agent's insights?",
        ]
        critic_name = "critic"
        critic = Critic(
            critic_name,
            f"You are the {critic_name}. You give a rating on from 1 to 5 on the {instagram_publisher_name} suggestions. The rating is based on the following list: {criteria_list}. You will give concrete suggestions if the score is under 5. You should also check that {instagram_publisher_name} sticks to the theme: {theme}. IMPORTANT: make sure the text is suitable for a instagram caption! You will pause and wait for user feedback after giving 4 / 5 or above. If the output is not in the format of a single string with hashtags at the end, you will ask the tweeter correct it.",
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy", code_execution_config=False
        )

        group_chat = autogen.GroupChat(
            agents=[analytics_agent, instagram_publisher_agent, critic_agent, user_proxy], messages=[], max_round=10
        )

        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.config.autogen_config_list},
        )

        # Start prompt
        user_proxy.initiate_chat(
            manager,
            message=f"write an Instagram caption based on the following theme: {theme} that is somehow related to Gin or to the Gin produces Stookers Gin. The output should be text with hashtags at the end. I want the hashtags: #Stookers #Amsterdam to always be present. Do not thank each other for the feedback.",
        )

        instagram_caption = ""
        for v in user_proxy._oai_messages.values():
            instagram_caption = v[-2]["content"]

        team_image = TeamImage(instagram_caption)
        filename = team_image.create_image("instagram_images")

        print("INSTAGRAM CAPTION: ", instagram_caption)
        print("IMAGE PATH: ", filename)
        publisher = InstagramPublisher()
        publisher.publish(filename, instagram_caption)