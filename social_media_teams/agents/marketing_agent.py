from agent.abstract_agent import AbstractAgent
from configs.prompt_config import *
import sys
sys.path.append('../../agent')


class MarketingAgent(AbstractAgent):
    def __init__(self, name: str, system_message: str, agent_config: object, temperature=0.5) -> None:
        llm_config = {
            "config_list": agent_config,
            "timeout": 120,
            "temperature": 0.4,
            "frequency_penalty": 0.2
        }

        AbstractAgent.__init__(self, name, system_message, llm_config)

    def __str__(self) -> str:
        return "Marketing Agent"
