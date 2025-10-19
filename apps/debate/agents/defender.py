from crewai import Agent, LLM
from decouple import config
import os

# Ensure your Groq API key is set
os.environ["GROQ_API_KEY"] = config('GROQ_API_KEY')

# Defender: moderate reasoning model
llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.7)

def create_defender_agent(agents_config) -> Agent:
    return Agent(
        config=agents_config['defender_agent'],
        llm=llm
    )
