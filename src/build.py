import os
import pathlib
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from src.prompts import get_weather_prompt
from src.tools import get_weather_data
from dotenv import load_dotenv

def agent():
    load_dotenv()

    API_KEY = os.getenv("GEMINI_API_KEY")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0,
        max_tokens=1000,
        google_api_key=API_KEY
    )
    

    prompt = get_weather_prompt()
    tools = [get_weather_data]

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    return agent_executor


