import autogen

# from agents.researcher import Researcher
from research_teams.agents.researcher import Researcher
from research_teams.agents.critic import Critic
from research_teams.scraper import Scraper
from enums.platform import Platform
import logging

# TODO: Add logging
logger = logging.getLogger(__name__)


class TwitterResearchTeam:
    def __init__(self, theme: str, autogen_config: object):
        self.theme = theme
        self.autogen_config = autogen_config

    def research_results(self) -> str:
        scraper = Scraper(self.theme, Platform.TWITTER)
        scraped_data = scraper.scrape()

        # Create the Researcher Agent
        researcher_name = "researcher"
        researcher = Researcher(
            researcher_name,
            f"You are the {researcher_name}. You will be given raw information with the theme of: {self.theme}. You will then use the information you find to write a short summary of the topic. After each iteration you will wait for the reviewer's feedback on the content. The information: "
            + str(scraped_data),
            self.autogen_config,
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
            self.autogen_config,
        )
        critic_agent = critic.retrieve_agent()

        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            code_execution_config=False,
        )

        group_chat = autogen.GroupChat(
            agents=[researcher_agent, critic_agent, user_proxy],
            messages=[],
            max_round=10,
        )

        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.autogen_config},
        )

        user_proxy.initiate_chat(
            manager,
            message=f"Distil the input information related to the theme: {self.theme} into four elements: 1. insights 2.fun facts 3.recepies 4. something related to Stookers gin. Do not thank each other for the feedback.",
        )

        for v in user_proxy._oai_messages.values():
            result = v[-2]["content"]

        return result

    def __str__(self):
        return "TwitterResearchTeam"
