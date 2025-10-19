from crewai import Agent, LLM
from decouple import config
import os

os.environ["GROQ_API_KEY"] = config('GROQ_API_KEY')

# Judge: stronger reasoning model
llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.5)

def create_judge_agent(agents_config) -> Agent:
    return Agent(
        config=agents_config['judge_agent'],
        llm=llm
    )
