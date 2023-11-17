import autogen
import logging
from configs.app_config import AppConfig
from research_teams.scraper import Scraper
from enums.platform import Platform
from research_teams.agents.researcher import Researcher
from research_teams.agents.critic import Critic
from configs.app_config import AppConfig

# TODO: Add logging
logger = logging.getLogger(__name__)


class ResearchTeam:
    def __init__(self, theme:str, platform: Platform):
        self.platform = platform
        self.theme = theme
        self.config = AppConfig()

    def research_results(self) -> str:
        scraper = Scraper(self.theme)
        scraped_platform_data = scraper.scrape(
            Platform.INSTAGRAM
        )  # TODO: have the scraper save the data to a file, then use a RAG agent to learn from the data
        scraped_web_data = scraper.scrape(Platform.WEB)

        # Create the Researcher Agent
        researcher_name = "researcher"
        researcher = Researcher(
            researcher_name,
            f"You are the {researcher_name}. You will be given raw information with the theme of: {self.theme}. You will then use the information you find to write a short summary of the topic. After each iteration you will wait for the reviewer's feedback on the content. The information: {str(scraped_platform_data)} and \n {str(scraped_web_data)}",
            self.config.autogen_config_list,
        )
        researcher_agent = researcher.retrieve_agent()

        # Create the Critic Agent
        criteria_list = [
            "Is the text relevant to the topic?",
            "Is the text grammatically correct?",
            "Is the text concise?",
            "Based on the knowledge you have, are the facts correct?",
        ]
        critic_name = "critic"
        critic = Critic(
            critic_name,
            f"You are the {critic_name}. You give a rating on from 1 to 5 on the researchers suggestions. The rating is based on the following list: {criteria_list}. You will give concrete suggestions if the score is under 5. You will give feedback if the result does not have four pointer, containing the criteria given by the user_proxy You will pause and wait for user feedback after giving 4 / 5 or above.",
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # Create the User Proxy Agent
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            code_execution_config=False,
        )

        # Create the Group Chat
        group_chat = autogen.GroupChat(
            agents=[researcher_agent, critic_agent, user_proxy],
            messages=[],
            max_round=10,
        )

        # Create the Group Chat Manager
        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.config.autogen_config_list},
        )

        user_proxy.initiate_chat(
            manager,
            message=f"Distil the input information related to the theme: {self.theme} into four elements: 1. insights 2.fun facts 3.recepies 4. something related to Stookers gin. Do not thank each other for the feedback.",
        )

        # Get results
        for v in user_proxy._oai_messages.values():
            result = v[-2]["content"]

        return result

    def __str__(self):
        return "Research Team"
