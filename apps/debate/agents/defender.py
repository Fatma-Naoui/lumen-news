from crewai import Agent, LLM
from decouple import config
import os

os.environ["GROQ_API_KEY"] = config('GROQ_API_KEY')

# OPTIMIZED: Faster model with token limit
llm = LLM(
    model="groq/llama-3.1-8b-instant",  # Faster, cheaper
    temperature=0.7,
    max_tokens=500  # ✅ LIMIT TOKENS - Forces concise responses
)

def create_defender_agent(agents_config) -> Agent:
    return Agent(
        config=agents_config['defender_agent'],
        llm=llm,
        max_iter=1  # ✅ Prevent loops
    )