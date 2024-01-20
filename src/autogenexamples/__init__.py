"""
Autogen is a framework by Microsoft that allows you to build coorparative AI agents to solve a task
The agents converse to solve the task and each individual agetn is customizable, they employ a combination of LLMs, human inputs and tools.

It supports:
- Agent customization
- Multi agent conversation
- flexible conversation patterns

Auto gen allows building next-gen LLM applications based on mult-agent conversations
Auto gen offers optimization techniques such as API unification, caching, error handling, multi-config inference, context programmming

Autogen offers a unified muli-agent conversation framework as a high level abstracion of using foundation models. It features capable, customizable and conversable agents which integrate with LLMs, tools and humans via automated agent chats. 
By automating chat among multi capable agents one can easily make them collectively perform autonomously or with human feedbac, including toask that require using tools via code. 

This framework simplifies the orchestration, automation and optimizaiton of complex LLM workflow

Agetn is an abstraction which uses an LLM to solve a task through interagent conversations. 
- Conversation
- Customization 

* ConversableAgent: Base class for agent capable of covnersing with other agetns though which the task is jointly finished. An 
agent can communicate with other agents to complete a task. Different agents can differ in what tasks they perform after receiving messages. 

* AssitantAgent: This is a sub class of the ConversableAgent designed to work as an AI asssistant. It performs the task but can not execute it. It requires
a user or user agent to execute the task. 

* UserProxyAgent: This is a subclass of the ConversableAgent, conceptually it is a proxy  aget for the human, soliciting huma input as the agent's reply at each interaction. It also has 
the abilitty to execute code and call functions or tools. Code execution can be disabled. LLM-based response is disabled by default, but can be enabled. 
"""

