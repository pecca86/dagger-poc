import autogen
import logging
from configs.app_config import AppConfig
from research_teams.scraper import Scraper
from enums.platform import Platform
from research_teams.agents.researcher import Researcher
from research_teams.agents.critic import Critic
from configs.app_config import AppConfig
from configs.prompt_config import *

# TODO: Add logging
logger = logging.getLogger(__name__)


class ResearchTeam:
    def __init__(self, theme:str, platform: Platform):
        self.platform = platform
        self.theme = theme
        self.config = AppConfig()
        logging.info("** PHASE: Twitter Research **")

    def research_results(self) -> str:
        scraper = Scraper(self.theme)
        scraped_platform_data = scraper.scrape(
            Platform.INSTAGRAM
        )  # TODO: have the scraper save the data to a file, then use a RAG agent to learn from the data
        scraped_web_data = scraper.scrape(Platform.WEB)

        # Create the Researcher Agent
        # TODO: Turn in to a RAG agent
        researcher_name = "researcher"
        researcher = Researcher(
            researcher_name,
            instagram_research_agent['prompt'].replace("{researcher_name}", researcher_name).replace("{theme}", self.theme),
            self.config.autogen_config_list,
        )
        researcher_agent = researcher.retrieve_agent()

        # Create the Critic Agent
        criteria_list = str(instagram_research_critic['criteria_list'])
        critic_name = instagram_research_critic['name']
        critic = Critic(
            critic_name,
            instagram_research_critic['prompt'].replace("{critic_name}", critic_name).replace("{criteria_list}", criteria_list),
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
            message=instagram_research_user['prompt'].replace("{theme}", self.theme),
        )

        # Collect logs:
        msg_dic = manager._oai_messages
        for k, v in msg_dic.items():
            logging.info("\n\nFull Conversation: \n")
            for item in v:
                logging.info(f"[{item['name']}]: {item['content']}\n")
            break

        # Get results
        for v in user_proxy._oai_messages.values():
            result = v[-2]["content"]

        return result

    def __str__(self):
        return "Research Team"
