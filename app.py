from src.build import agent

if __name__ == "__main__":
    agent_executor = agent()
    while True:
        q = input("City/cities (or 'q' to quit): ").strip()
        if q.lower() == "q":
            break
        print(agent_executor.invoke({"input": f"Weather in {q}"})["output"])