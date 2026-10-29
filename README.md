# Weather Agent 🌦️

A LangChain-powered AI agent that answers natural-language weather questions using a ReAct (Reason + Act) loop. You send it a city name via a REST API, and it autonomously decides to call the Weatherstack API, interprets the result, and returns a human-readable weather summary.

## Features

- **ReAct agent** — uses a Thought → Action → Observation loop to decide when and how to fetch weather data.
- **REST API** — a single `POST /chat` endpoint built with FastAPI; accepts a city name and returns the agent's answer.
- **Tool-based architecture** — weather fetching is wrapped as a LangChain `@tool`, making it easy to add more tools later.
- **Prompt-driven behaviour** — the agent's system prompt is defined in a dedicated module and follows the standard ReAct template.

## How It Works

```
User ──POST {"city":"Delhi"}──▶ app.py (/chat)
                                   │
                                   ▼
                           src/build.py  →  agent()
                           ├─ loads .env (GEMINI_API_KEY)
                           ├─ creates ChatGoogleGenerativeAI (gemini-3.8-flash)
                           ├─ gets ReAct prompt from src/prompts.py → get_weather_prompt()
                           ├─ registers src/tools.py → get_weather_data as a tool
                           └─ returns an AgentExecutor
                                   │
                          .invoke({"input": "Weather in Delhi"})
                                   │
                                   ▼
                        Agent enters ReAct loop:
                        Thought → Action: get_weather_data("Delhi")
                                   │
                                   ▼
                        src/tools.py → calls Weatherstack API
                        (uses WEATHERSTACK_API_KEY)
                                   │
                                   ▼
                        Observation: "Temperature: 26°C, Clear, Humidity: 45%"
                                   │
                                   ▼
                        Thought → Final Answer
                                   │
                                   ▼
                        Response ──▶ User
```

1. **`app.py`** — FastAPI entry point. Defines a `POST /chat` endpoint that accepts `{"city": "<name>"}`.
2. **`src/build.py`** → `agent()` — Loads environment variables, initialises the Gemini LLM, assembles the ReAct prompt and tool list, and returns a LangChain `AgentExecutor`.
3. **`src/prompts.py`** → `get_weather_prompt()` — Returns a `PromptTemplate` with the ReAct format (Question / Thought / Action / Observation / Final Answer).
4. **`src/tools.py`** → `get_weather_data(city)` — A LangChain `@tool` that calls the [Weatherstack current-weather API](https://weatherstack.com/) and returns temperature, description, and humidity.

## Tech Stack

| Category       | Technology                                                                 |
|----------------|---------------------------------------------------------------------------|
| LLM            | Google Gemini 3.8 Flash (via `langchain-google-genai`)                    |
| Agent framework| LangChain (`langchain`, `langchain-classic`, `langchain-core`)            |
| Agent pattern  | ReAct (`create_react_agent` + `AgentExecutor` from `langchain-classic`)   |
| Weather data   | [Weatherstack API](https://weatherstack.com/) (current weather endpoint)  |
| Web framework  | FastAPI + Uvicorn                                                         |
| HTTP client    | `requests`                                                                |
| Config         | `python-dotenv`                                                           |
| Language       | Python 3.11+                                                              |

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Bhoware/Weather-agent.git
cd Weather-agent

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file in the project root with these variables
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
WEATHERSTACK_API_KEY=your_weatherstack_api_key_here
```

| Variable              | Where to get it                                                      |
|-----------------------|----------------------------------------------------------------------|
| `GEMINI_API_KEY`      | [Google AI Studio](https://aistudio.google.com/apikey)               |
| `WEATHERSTACK_API_KEY`| [Weatherstack](https://weatherstack.com/) — free tier available      |

## Usage

Start the server:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

**Example request:**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"city": "Delhi"}'
```

**Example response:**

```json
{
  "output": "The current weather in Delhi, India is Clear with a temperature of 26°C and a humidity level of 45%."
}
```

Interactive API docs are auto-generated at `http://127.0.0.1:8000/docs` (Swagger UI).

## Project Structure

```
Weather-agent/
├── app.py                    # FastAPI entry point — POST /chat endpoint
├── src/
│   ├── __init__.py           # Makes src a Python package
│   ├── build.py              # Assembles the ReAct agent and returns AgentExecutor
│   ├── prompts.py            # ReAct prompt template for the weather assistant
│   └── tools.py              # @tool: get_weather_data — calls Weatherstack API
├── research/
│   ├── demo.ipynb            # Jupyter notebook used during development/prototyping
│   └── .env                  # Notebook-local env file (git-ignored)
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI — installs deps and runs pytest
├── .env                      # API keys (git-ignored — you create this)
├── .gitignore                # Ignores .env, __pycache__/, venv/
├── requirements.txt          # Pinned Python dependencies
└── README.md                 # This file
```

## Limitations

- **Current weather only** — the Weatherstack free tier and the tool implementation only fetch current conditions, not forecasts.
- **Single tool** — the agent has access to only one tool (`get_weather_data`). It cannot answer non-weather questions.
- **No input validation beyond city name** — the endpoint accepts any string as a city; invalid names produce a generic error from the Weatherstack API.
- **API rate limits** — both the Gemini API and Weatherstack API have rate limits (especially on free tiers). Heavy usage may result in `500` errors.
- **No authentication on the API** — the FastAPI endpoint is open; there's no API key or auth middleware protecting it.
- **Agent is re-created per request** — `agent()` in `build.py` is called on every request, re-loading `.env` and re-initialising the LLM each time. This adds latency.
- **No tests in the repo yet** — the CI pipeline (`ci.yml`) runs `pytest`, but no test files are present.

## Live Demo

> TODO: add deployed link

## Author

**Anshul** — [github.com/Bhoware](https://github.com/Bhoware)
