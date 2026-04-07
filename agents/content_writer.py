import os
from crewai import Agent, LLM
from crewai_tools import FileWriterTool

import os
import streamlit as st

def get_secret(key):
    return os.getenv(key) or st.secrets.get(key)


# LLM configurations - Agent specific config
model = os.getenv("WRITER_AGENT_LLM")
temperature = float(os.getenv("WRITER_AGENT_TEMPERATURE"))

llm = LLM(
    model=model,
    temperature=temperature
)

content_writer_agent = Agent(
    role="Content Writer",
    goal="Create comprehensive, well-structured reports and summaries",
    backstory = (
                "You are a professional content writer with expertise in creating "
                "clear, engaging, and well-structured documents. You can transform complex "
                "information into accessible and compelling content."
            ),
    llm=llm,
    tools=[FileWriterTool()],
    verbose=True,
)
