import os

import pandas as pd
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_experimental.agents.agent_toolkits.pandas.base import (
    create_pandas_dataframe_agent,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

llm_gpt = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
llm_claude_opus = ChatAnthropic(model_name="claude-3-opus-20240229", temperature=0)
llm_claude_haiku = ChatOpenAI(
    model_name="claude-3-haiku-20240307",
    temperature=0,
)
selected_llm = llm_gemini

# summarize data


def summerize_csv(filename):

    df = pd.read_csv(filename, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(
        llm=selected_llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True,
        agent_executor_kwargs={"handle_parsing_errors": "True"},
    )

    data_summary = {}

    data_summary["initial_data_sample"] = df.head()

    data_summary["column_descriptions"] = pandas_agent.run(
        f"Create a table in for dataset columns. Write a column name and column descriptions as a table format"
    )

    data_summary["missing_values"] = pandas_agent.run(
        "Is there any missing values in dataset and how many? Your response should be like 'There are X number of missing values in this dataset' replace missing values to 'X'"
    )

    data_summary["dupplicate_values"] = pandas_agent.run(
        "Is there any duplicate values in dataset and how many? Your response should be like 'There are X number of dupplicate values in this dataset' replace missing values to 'X'"
    )

    data_summary["essential_metrics"] = df.describe()

    return data_summary


# get dataframe


def get_dataframe(filename):

    df = pd.read_csv(filename, low_memory=False)
    return df


# analyze trend


def analyze_trend(filename, variable):

    df = pd.read_csv(filename, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(
        llm=selected_llm,
        df=df,
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": "True"},
        allow_dangerous_code=True,
        
    )

    trend_response = pandas_agent.run(
        f"Interpret the trend of this shortly: {variable}. Do not reject the interpretation!. The rows of the dataset is historical. So you can do interpreting with looking the rows of dataset"
    )

    return trend_response


# ask question


def ask_question(filename, question):

    df = pd.read_csv(filename, low_memory=False)

    pandas_agent = create_pandas_dataframe_agent(
        llm=selected_llm,
        df=df,
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": "True"},
        allow_dangerous_code=True,
    )

    AI_response = pandas_agent.run(question)

    return AI_response
