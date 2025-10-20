from crewai import Agent, LLM
from decouple import config
import os

os.environ["GROQ_API_KEY"] = config('GROQ_API_KEY')

# OPTIMIZED: Stronger model with MORE tokens for XAI explanation
llm = LLM(
    model="groq/llama-3.3-70b-versatile",  # Keep stronger model for judge
    temperature=0.3,  # ✅ Lower temp for consistent judgments
    max_tokens=800  # ✅ More tokens for detailed XAI reasoning
)

def create_judge_agent(agents_config) -> Agent:
    return Agent(
        config=agents_config['judge_agent'],
        llm=llm,
        max_iter=1
    )