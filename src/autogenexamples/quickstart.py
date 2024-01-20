from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}) # use_docker can be set to true to run the application in docker
print(user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD"))