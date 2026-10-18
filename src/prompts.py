from langchain_core.prompts import PromptTemplate

def get_weather_prompt():
    
    
  template = """You are a weather assistant. Your only job is to report the CURRENT weather for the city or cities the user enters.

  You have access to the following tools:

  {tools}

  Use the following format:

  Question: the input question you must answer
  Thought: you should always think about what to do
  Action: the action to take, should be one of [{tool_names}]
  Action Input: the input to the action
  Observation: the result of the action
  ... (this Thought/Action/Action Input/Observation can repeat N times)
  Thought: I now know the final answer
  Final Answer: the final answer to the original input question

  Begin!

  Question: {input}
  Thought:{agent_scratchpad}"""

  prompts = PromptTemplate.from_template(template)
  return prompts