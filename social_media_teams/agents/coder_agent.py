from agent.abstract_agent import AbstractAgent
import sys
sys.path.append('../../agent')

class CoderAgent(AbstractAgent):
    def __init__(self, name: str, system_message: str, agent_config: object, temperature=0) -> None:
        llm_config = {
            "config_list": agent_config,
            "timeout": 120,
            "temperature": temperature,
            "frequency_penalty": 0,
        }

        AbstractAgent.__init__(self, name, system_message, llm_config)

    def __str__(self) -> str:
        return "CoderAgent"