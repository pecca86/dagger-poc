import autogen

class AbstractAgent:
    def __init__(self, name, system_message, agent_config) -> None:
        self.name = name
        self.system_message = system_message
        self.agent_config = agent_config

        def create_agent(self):
            return autogen.AssistantAgent(
                name=self.name,
                system_message=self.system_message,
                llm_config=self.agent_config,
            )
        
        self.agent = create_agent(self)

    def retrieve_agent(self):
        self.agent.reset()
        return self.agent
    
    def __str__(self):
        return "agent"