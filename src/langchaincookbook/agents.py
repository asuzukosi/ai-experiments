from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from operator import itemgetter
import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, tool
from langchain.agents.output_parsers import XMLAgentOutputParser

load_dotenv()
model = ChatOpenAI()

@tool
def search(query: str) -> str:
    """
    Search things about current events
    """
    return "32 degrees"


tool_list = [search]

prompt = hub.pull("hwchase17/xml-agent-convo") # wtf does this mean?


def convert_intermediate_steps(intermediate_steps):
    log = ""
    for action, observation in intermediate_steps:
        log += (
            f"<tool>{action.tool}</tool><tool_input>{action.tool_input}</tool_input><observation>{observation}</observation>"
        )
    return log


def convert_tools(tools):
    return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])


agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: convert_intermediate_steps(x["intermediate_steps"])
    }
    | prompt.partial(tools=convert_tools(tool_list))
    | model.bind(stop=["</tool_input>", "</final_anser>"])
)

agent_executor = AgentExecutor(agent=agent, tools=tool_list, verbose=True)
agent_executor.invoke({"input": "Whats the weather in New York?"})