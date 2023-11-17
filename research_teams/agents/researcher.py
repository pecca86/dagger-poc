import sys
sys.path.append('../../agent')
from agent.abstract_agent import AbstractAgent

class Researcher(AbstractAgent):
    def __init__(self, name:str, system_message:str, agent_config:object, temperature=0):
        llm_config = {
            "config_list": agent_config,
            "timeout": 120,
            "temperature": temperature,
        }

        AbstractAgent.__init__(self, name, system_message, llm_config)

    def __str__(self) -> str:
        return "Researcher"