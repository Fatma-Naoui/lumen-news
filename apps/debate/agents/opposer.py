from crewai import Agent, LLM
from decouple import config
import os

os.environ["GROQ_API_KEY"] = config('GROQ_API_KEY')

# Opposer: similar strength to defender
llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0.7)

def create_opposer_agent(agents_config) -> Agent:
    return Agent(
        config=agents_config['opposer_agent'],
        llm=llm
    )
