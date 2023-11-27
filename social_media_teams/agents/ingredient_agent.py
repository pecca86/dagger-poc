from agent.abstract_agent import AbstractAgent
from configs.prompt_config import *
import sys
sys.path.append('../../agent')


class IngredientAgent(AbstractAgent):
    def __init__(self, name: str, system_message: str, agent_config: object, temperature=0.5) -> None:
        llm_config = {
            "config_list": agent_config,
            "timeout": 120,
            "temperature": instagram_prompts['ingredient_agent']['config']['temperature'],
            "frequency_penalty": instagram_prompts['ingredient_agent']['config']['frequency_penalty'],
        }

        AbstractAgent.__init__(self, name, system_message, llm_config)

    def __str__(self) -> str:
        return "Instagram Ingredient Agent"
