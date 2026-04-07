import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

import os
import streamlit as st

def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)

# LLM configurations - Agent specific config
model = get_secret("RESEARCH_AGENT_LLM")
temperature = float(get_secret("RESEARCH_AGENT_TEMPERATURE"))

llm = LLM(
    model=model,
    temperature=temperature
)

research_specialist_agent = Agent(
    role="Research Specialist",
    goal="Gather comprehensive and accurate information on given topics from multiple sources",
    backstory = (
                "You are an expert research specialist with years of experience in information gathering "
                "and fact-checking. You have a keen eye for reliable sources and can quickly identify the "
                "most relevant and up-to-date information on any topic."
            ),
    llm=llm,
    tools=[SerperDevTool()],
    verbose=True,
)
