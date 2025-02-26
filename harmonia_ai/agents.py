from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

class AgentFactory:
    def __init__(self, llm: BaseChatModel):
        """Initialize the factory with LLM and database connection.

        Args:
            llm (BaseChatModel): Language model instance
            db (Any, optional): Database connection. Defaults to None.
        """
        self.llm = llm
        self._initialize_tools()

    def _initialize_tools(self):
        """Initialize all available tools."""
        self.chef_tools = []
        self.trainer_tools = []
        self.mental_coach_tools = []
        

    def create_agent(self, agent_type: str) -> Any:
        """Create and return an agent based on the given type.

        Args:
            agent_type (str): Type of agent to create

        Returns:
            Any: Created agent instance
        """
        agent_creators = {
            "chef": self._create_chef_agent,
            "trainer": self._create_trainer_agent,
            "mental_coach": self._create_mental_coach_agent,
        }
        creator = agent_creators.get(agent_type)
        if not creator:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return creator()

    def _create_chef_agent(self):
        """Create web search agent."""
        return create_react_agent(
            self.llm,
            tools=[],
            state_modifier="""You are a personal chef.""",
        )

    def _create_trainer_agent(self):
        """Create training agent."""
        return create_react_agent(
            self.llm,
            tools=[],
            state_modifier="""You are a personal trainer.""",
        )
    
    def _create_mental_coach_agent(self):
        """Create mental coach agent."""
        return create_react_agent(
            self.llm,
            tools=[],
            state_modifier="""You are a mental coach.""",
        )
