from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from src.build import agent


app=FastAPI()

class Input(BaseModel):
    city:str

@app.post("/chat")
def weather_agent(input: Input):
    try:
        agent_executor = agent()
        return {"output": agent_executor.invoke({"input": f"Weather in {input.city}"})["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    