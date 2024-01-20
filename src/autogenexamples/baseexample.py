from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from typing import Literal
from pydantic import BaseModel, Field
from typing_extensions import  Annotated


config_list = config_list_from_json("OAI_CONFIG_LIST", 
                                    filter_dict={
                                        "model": ["gpt-3.5-turbo"]
                                    })

# # create an AssistatnAgent intance named "assistant"
# assistant = AssistantAgent(name="assistant")

# # create a UserProxyAgent instance named "user_proxy"
# user_proxy = UserProxyAgent(name="user_proxy")


"""
ConversableAgent.register_for_llm - is used to register the function as a 
Tool in the llm_config of a ConversableAgent. 
The ConversableAgent agent can propose execution of a 
registered Tool, but the actual execution will be performed by a 
UserProxy agent.


ConversableAgent.register_for_execution is used to register the function 
in the function_map of a UserProxy agent.

"""

llm_config = {
    "config_list": config_list,
    "timeout": 120
}

chatbot = AssistantAgent(
    name="chatbot",
    system_message="For currency exachang tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10
)

CurrencySymbol = Literal["USD", "EUR"]

def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1/1.1
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f'Unknown currencies {base_currency}, {quote_currency}')
    
class Currency(BaseModel):
    currency: Annotated[CurrencySymbol, Field(..., description="Currency symbol")]
    amount: Annotated[float, Field(0, description="Amount of currency", ge=0)]


@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
    base_amount: Annotated[float, "Amout of currency in base currency"],
    base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
    quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
    
) -> Currency:
    quote_maount = exchange_rate(base_currency, quote_currency) * base_amount
    return Currency(amount=quote_maount, currency=quote_maount)


user_proxy.initiate_chat(
    chatbot,
    message="How much is 123.45 USD in EUR?",
)