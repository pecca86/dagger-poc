import sys
sys.path.append('../../agent')
from agent.abstract_agent import AbstractAgent

class Critic(AbstractAgent):
    def __init__(self, name, system_message, agent_config, temperature=0):
        llm_config = {
            "config_list": agent_config,
            "timeout": 120,
            "temperature": temperature,
        }

        AbstractAgent.__init__(self, name, system_message, llm_config)

    def __str__(self):
        return "Critic"