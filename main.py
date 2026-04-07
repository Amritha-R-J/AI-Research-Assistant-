from dotenv import load_dotenv
load_dotenv()

from crew import research_crew

import os
import streamlit as st

def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)

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
