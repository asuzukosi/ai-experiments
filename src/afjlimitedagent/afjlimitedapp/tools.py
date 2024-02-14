import pickle
import pandas as pd
from llama_index.llms.openai import OpenAI
from llama_index.service_context import ServiceContext
from llama_index.query_engine.pandas import PandasQueryEngine
from ingest_data import DATA_DIRECTORY, load_dataset, postprocess_dataset
from langchain import hub
from textwrap import dedent
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import create_openai_functions_agent
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain_core.prompts.chat import ChatPromptTemplate
from pydantic.v1 import BaseModel, Field
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.indices.list.base import SummaryIndex
from llama_index.storage import StorageContext
from llama_index.indices.loading import load_index_from_storage
from langchain.tools import tool
import json
import os
from json import JSONDecodeError

brands = ['Seat']
models = ['Leon']
locations = ['CW', 'RT', 'S', 'KA', 'BB']
conditions = ['Normal',
  'Free',
  'Traffic',
  'Emergency Braking',
  'Normal Icy Road',
  'Free Accelaration',
  'Traffic Jam Measurement error']

# transform brand
def transform_brand(brand):
    return brands.index(brand)

def transform_model(model):
    return models.index(model)

def transform_location(location):
    return locations.index(location)

def transform_condition(condition):
    return conditions.index(condition)

def get_arima_model():
    with open('../arima_model.pkl', 'rb') as f:
        fit_model = pickle.load(f)
        return fit_model
    
def get_random_forest_model():
    with open('../random_forest_model.pkl', 'rb') as f:
        rf_classifier = pickle.load(f)
        return rf_classifier
    
    
def get_data_for_arima_model(engine_coolant_temp, intake_manifold_pressure, engine_rpm, source, destination, condition):
    # Create a dictionary with the data for the single entry
    data = {
        'Engine Coolant Temperature [°C]': [engine_coolant_temp],
        'Intake Manifold Absolute Pressure [kPa]': [intake_manifold_pressure],
        'Engine RPM [RPM]': [engine_rpm],
        'source': [source],
        'destination': [destination],
        'condition': [condition],
    }

    # Create the DataFrame
    df = pd.DataFrame(data)
    return df


def get_data_for_categorical_model(vehicle_speed, source, destination, hour, minute):
    # Create a DataFrame with a single row and specified columns
    data = {
        'Vehicle Speed Sensor [km/h]': [vehicle_speed],
        'source': [source],
        'destination': [destination],
        'hour': [hour],
        'minute': [minute]
    }

    df = pd.DataFrame(data)
    return df

ARIMA_MODEL = get_arima_model()
RANDOM_FOREST_MODEL = get_random_forest_model()


def infer_arima_model(X):
    forcast = ARIMA_MODEL.forecast(steps=len(X), exog=X[['Engine Coolant Temperature [°C]',
                                        'Intake Manifold Absolute Pressure [kPa]', 'Engine RPM [RPM]', 'source',
                                        'destination', 'condition']])
    return forcast.iloc[0]


def infer_forest_model(X):
    # Make predictions on the testing data
    y_pred = RANDOM_FOREST_MODEL.predict(X)
    return y_pred[0]

# get llm context
li_llm = OpenAI(model="togethercomputer/CodeLlama-34b-Instruct")
lc_llm = ChatOpenAI(model="togethercomputer/CodeLlama-34b-Instruct", temperature=0.1)

service_context = ServiceContext.from_defaults(llm=li_llm)

# load dataset 
def get_dataset():
    if os.path.exists("full_dataframe.pkl"):
        print("Loading dataset")
        with open("full_dataframe.pkl", "rb") as f:
            df = pickle.load(f)
            return df
    else:
        print("creating dataset")
        df = load_dataset(DATA_DIRECTORY)
        df = postprocess_dataset(df)
        with open("full_dataframe.pkl", "wb") as f:
            pickle.dump(df, f)
        return df

df = get_dataset()
# get dataset query engine
query_engine_with_sythesis =  PandasQueryEngine(df=df, 
                                                service_context=service_context, 
                                                verbose=True, 
                                                synthesize_response=True)

diagraming_agent = create_pandas_dataframe_agent(llm=lc_llm,
                                                 df=df,
                                                 verbose=False)
def query_diagraming_agent(query):
    prompt = dedent(
        """
            [INST]
            You are a python diagraming agent. You make use of use of matplotlib and a dataframe named
            df to plot diagrams based on user queries.
            
            For the following query, you will output a python code snippet that makes use of a dataframe named df
            and matplotlib to plot either a bar chart or a line chart. 
            
            You must create a fig object for diagrams and at the end of the diagram wrap the figure in a 
            `st.pyplot(fig)` instruction. This should be the last instruction of the generated code
            
            Your output should be python code wrapped in quote strings.

            Lets think step by step.

            Below is the query.
            Query: 
            
            [/INST]
            """
        + query
    )

    # Run the prompt through the agent.
    response = diagraming_agent.run(prompt)
    return response.__str__()


storage_context = StorageContext.from_defaults(persist_dir="../afjlimitedweb")
index = load_index_from_storage(storage_context)

company_query_engine = index.as_query_engine(service_context=service_context)

openai_fn_agent_prompt: ChatPromptTemplate = hub.pull("hwchase17/openai-functions-agent")

class DataSetQuestionAnswerSchema(BaseModel):
    """ 
    Schema to be used when asking questions about the dataset
    """
    query:str = Field(description="query question to be asked about the dataset")
    
    
@tool("dataset-question-answer", args_schema=DataSetQuestionAnswerSchema, return_direct=True)
def dataset_question_answer(query:str):
    """
    Provides answer to any question asked about the dataset. 
    It takes a natural language question about the dataset and provides a natural language response.
    """
    response = query_engine_with_sythesis.query(query)
    # response = query_engine_with_sythesis.query(query)
    # return str(response.response)
    return response.response


class DataSetDiagramRequestSchema(BaseModel):
    """
    Schema to used when requesting to draw a diagram from the dataset
    """
    query:str = Field(description="query describing type and nature of diagram to be drawn")
    
    
@tool("dataset-diagram-tool", args_schema=DataSetDiagramRequestSchema, return_direct=False)
def dataset_diagram_request(query: str):
    """ 
    Draws diagram for information about the dataset
    It takes a natural language diagram request and draws the diagram
    """
    # response = query_diagraming_agent(query)
    # return response
    try:
        response = query_diagraming_agent(query)
        return "diagram drawn"
    except Exception as e:
        return "failed to draw diagram"
    
    

class VehicleVelocityPredictionSchema(BaseModel):
    engine_coolant_temp: float = Field(description="The engine coolant temperature of the vehicle")
    intake_manifold_pressure: float = Field(description="The Intake manifold absolute pressure of the vehicle")
    engine_rpm: float = Field(description="The engine rpm of the vehicle")
    source: str = Field(description="The source location of the vehicle")
    destination: str = Field(description="The destination location of the vehicle")
    condition: str = Field(description="The condition of the vehicle, must be one of the following: 'Normal','Free', 'Traffic', 'Emergency Braking','Normal Icy Road','Free Accelaration','Traffic Jam Measurement error'")


@tool("predict-vehicle-velocity", args_schema=VehicleVelocityPredictionSchema, return_direct=False)
def predict_vehicle_velocity(engine_coolant_temp, intake_manifold_pressure, engine_rpm, source, destination, condition):
    """ 
    The function allows for predicting the vehicle velocity given the following fields:
    engine coolant temperature, intake manifold pressure, engine rpm, source, destination and condition
    """
    source = transform_location(source)
    destination = transform_location(destination)
    condition = transform_condition(condition)
    engine_coolant_temp = float(engine_coolant_temp)
    intake_manifold_pressure = float(intake_manifold_pressure)
    engine_rpm = float(engine_rpm)
    input_df = get_data_for_arima_model(engine_coolant_temp, intake_manifold_pressure, engine_rpm, source, destination, condition)
    result = infer_arima_model(input_df)
    return str(result) + " Km/h"


class VehicleConditionPredictionSchema(BaseModel):
    vechicle_speed:float = Field(description="Vehicle speed defines the speed the vehicle is moving at")
    source:str = Field(description="This is the source location of the vehicle")
    destination:str	= Field(description="This is the destination location of the vehicle")
    hour:int = Field(description="This is the hour the measurement was taken")
    minute:int = Field(description="This is the minute the measurement was taken")


@tool("predict-vehicle-condition", args_schema=VehicleConditionPredictionSchema, return_direct=False)
def predict_vehicle_condition(vehicle_speed, source, destination, hour, minute):
    """ 
    This tool is used to predict the condition of a vehicle given the vehicle speed, source location, destination location
    hour and minute of the measurement. It will uses this information to infer the current condition of the vehicle which could
    be one of the following:
    Normal,Free,Traffic,Emergency Braking,Normal Icy Road,Free Accelaration,Traffic Jam Measurement error
    """
    source = transform_location(source)
    destination = transform_location(destination)
    hour = int(hour)
    minute = int(minute)
    vehicle_speed = float(vehicle_speed)
    input_df = get_data_for_categorical_model(vehicle_speed, source, destination, hour, minute)
    prediction = infer_forest_model(input_df)
    return f"The predicted condition is {conditions[prediction]}"


class AFJLimitedQASchema(BaseModel):
    query: str = Field(description="This contains a question the user would like to ask about AFJ Limited")
    
@tool("afj-limited-qa", args_schema=AFJLimitedQASchema, return_direct=False)
def afj_limited_qa(query):
    """ 
    Answers questions related to AFJ Limited. Receives a query related to AFJ limited and 
    provides a natural language response
    """
    response = company_query_engine.query(query)
    return response.response


# create python repl tool
python_repl = PythonREPLTool(name="python-repl")


tools = [python_repl,
         dataset_question_answer, 
         dataset_diagram_request, 
         predict_vehicle_velocity,
         predict_vehicle_condition, 
         afj_limited_qa]

openai_agent = create_openai_functions_agent(lc_llm, tools, openai_fn_agent_prompt)
agent_executor = AgentExecutor(agent=openai_agent, tools=tools, verbose=True)

tool_map = { tool.name: tool for tool in tools }

def run_agent_executor(query):
    response = agent_executor.invoke({"input": query})
    try:
        output = json.loads(response["output"])
    except JSONDecodeError as e:
        return response["output"], "No function call"
    
    function_call = output[0]
    message = dedent(f"""
       function name : {function_call["name"]}
       function arguments : {function_call["arguments"]}
    """)
    
    try:
        fnc = tool_map[function_call["name"]]
        result = fnc.run(tool_input=function_call["arguments"])
        return result, message
    except Exception as e:
        return f"function call failed with error {e}", message
