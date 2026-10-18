from fastapi import FastAPI
from pydantic import BaseModel
from src.build import agent


app=FastAPI()

class Input(BaseModel):
    city:str

@app.post("/chat")
def weather_agent(input: Input):
    agent_executor = agent()
    return {"output": agent_executor.invoke({"input": f"Weather in {input.city}"})["output"]}


    