import datetime
import os
from typing import Any, Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command
from typing_extensions import TypedDict

from harmonia_ai.agents import AgentFactory

load_dotenv()

class State(MessagesState):
    next: str

class HarmoniA:
    def __init__(self):
        """Initialize the HarmoniA class."""
        self.llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agent_factory = AgentFactory(self.llm)
        self.memory = MemorySaver()
        self.graph = self._create_graph()

    def make_super_supervisor_node(self, members: list[str]) -> str:
        options = ["FINISH"] + members
        system_prompt = f"""You are a supervisor tasked with managing a conversation
            between the following workers: {members}. Use chat_tool to handle simple
            conversation, use web_search for searching the web, use researcher to
            generate report when asked. Given the following user request,
            respond with the worker to act next. Each worker will perform a
            task and respond with their results and status. When finished,
             respond with FINISH."""

        class Router(TypedDict):
            """Worker to route to next. If no workers needed, route to FINISH."""

            next: Literal[*options]

        def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
            """An LLM-based router."""
            messages = [
                {"role": "system", "content": system_prompt},
            ] + state["messages"]
            response = self.llm.with_structured_output(Router).invoke(messages)
            goto = response["next"]
            if goto == "FINISH":
                goto = END

            return Command(goto=goto, update={"next": goto})

        return supervisor_node

    def _create_agent_node(self, agent_type: str):
        """Create a node function for a specific agent type.

        Args:
            agent_type (str): Type of agent to create node for

        Returns:
            callable: Agent node function
        """
        agent = self.agent_factory.create_agent(agent_type)

        def agent_node(state: State) -> Command[Literal["supervisor"]]:
            result = agent.invoke(state)
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=result["messages"][-1].content, name=agent_type
                        )
                    ]
                },
                goto="supervisor",
            )

        return agent_node

    def conversation_node(self, state) -> Command[Literal["supervisor"]]:
        """Node for conversation with the user."""
        prompt = f"""You are HarmoniA, a conversational AI assistant. You will be
        assisting the user engaging with simple conversation, answering questions,
        and providing information. Your goal is to maintain a friendly and
        professional. Always be positive and helpful.

        Today's {datetime.datetime.now().strftime("%Y-%m-%d")}
        """
        response = self.llm.invoke(
            [{"role": "system", "content": state["messages"][-1].content + prompt}]
        )
        return Command(
            update={
                "messages": [
                    HumanMessage(content=response.content, name="conversation"),
                ]
            },
            goto="__end__",
        )


    def _create_graph(self):
        """Create and return the workflow graph.

        Returns:
            StateGraph: Compiled workflow graph
        """
        members = ["chef", "trainer", "mental_coach"]
        # Create the graph
        super_builder = StateGraph(State)

        # Add supervisor node that will handle role-based access
        supervisor_node = self.make_super_supervisor_node(
            members + ["chat_tool"]
        )
        super_builder.add_node("supervisor", supervisor_node)

        # Add all agent nodes (they will be selectively used based on role)
        for member in members:
            super_builder.add_node(member, self._create_agent_node(member))

        # Create researcher graph
        super_builder.add_node("chat_tool", self.conversation_node)

        # Add edges
        super_builder.add_edge(START, "supervisor")

        return super_builder.compile(checkpointer=self.memory)

    async def ask_harmonia(self, prompt: str, chat_id: str="0") -> Any:
        """Ask HarmoniA a question.

        Args:
            prompt (str): Prompt to ask HarmoniA

        Returns:
            Any: Response from HarmoniA
        """
        config = {"configurable": {"thread_id": chat_id}}
        try:
            async for response in self.graph.astream(
                {"messages": [HumanMessage(content=prompt)]},
                config,
                stream_mode="updates",
            ):
                print(response)
                if "supervisor" not in list(response.keys()):
                    messages = list(response.values())[0].get("messages", [])
                    if messages:
                        yield messages[0].content
        except Exception as e:
            yield f"Error in ask_harmonia: {e}"
