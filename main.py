from dotenv import load_dotenv
load_dotenv()

from crew import research_crew

def run(topic: str):
    result = research_crew.kickoff(inputs={"topic": topic})

    print("-"*50)
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    topic = (
        "AI Agents"
    )

    run(topic)