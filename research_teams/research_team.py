import autogen
import logging
from configs.app_config import AppConfig
from enums.platform import Platform
from configs.app_config import AppConfig
from configs.prompt_config import *

logger = logging.getLogger(__name__)


class ResearchTeam:
    def __init__(self, theme: str = None, platform: Platform = None):
        self.platform = platform
        self.theme = theme
        self.config = AppConfig()
        self.prompts = (
            instagram_prompts
            if self.platform == Platform.INSTAGRAM
            else twitter_prompts
        )  # TODO: needs to be changed if more platforms are introduced
        logging.info(f"** PHASE: {platform} Research **")

    def research_results(self) -> str:

        researcher_name = "researcher"
        researcher_agent = autogen.AssistantAgent(
            name=researcher_name,
            system_message=self.prompts["research_agent"]["prompt"]
            .replace("{researcher_name}", researcher_name)
            .replace("{theme}", self.theme),
            llm_config={
                "config_list": self.config.autogen_config_list,
                "temperature": instagram_prompts["research_agent"]["config"]["temperature"],
                "frequency_penalty": instagram_prompts["research_agent"]["config"]["frequency_penalty"],
                "timeout": 120,
            },
        )

        critic_name = self.prompts["research_critic"]["name"]
        critic_agent = autogen.AssistantAgent(
            name=critic_name,
            system_message=self.prompts["research_critic"]["prompt"]
            .replace("{critic_name}", critic_name)
            .replace("{theme}", self.theme),
            llm_config={
                "config_list": self.config.autogen_config_list,
                "temperature": instagram_prompts['publisher_critic']["config"]["temperature"],
                "frequency_penalty": instagram_prompts['publisher_critic']["config"]["frequency_penalty"],
                "timeout": 120,
            },
        )

        # Create the User Proxy Agent
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
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
            message=self.prompts["research_user"]["prompt"].replace(
                "{theme}", self.theme
            ),
        )

        # Collect logs:
        msg_dic = manager._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                logging.info(f"[{item['name']}]: {item['content']}\n")
            break

        # Get results
        for v in user_proxy._oai_messages.values():
            result = v[-2]["content"]

        return result

    def __str__(self):
        return "Research Team"
