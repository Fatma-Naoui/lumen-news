from crewai import Crew, Task
from crewai.project import CrewBase, agent, crew, task
from apps.debate.agents.defender import create_defender_agent
from apps.debate.agents.opposer import create_opposer_agent
from apps.debate.agents.judge import create_judge_agent

@CrewBase
class DebateCrew():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def defender_agent(self):
        return create_defender_agent(self.agents_config)

    @agent
    def opposer_agent(self):
        return create_opposer_agent(self.agents_config)

    @agent
    def judge_agent(self):
        return create_judge_agent(self.agents_config)

    @task
    def defend_task(self):
        return Task(
            config=self.tasks_config['defend_task'],
            agent=self.defender_agent()
        )

    @task
    def oppose_task(self):
        return Task(
            config=self.tasks_config['oppose_task'],
            agent=self.opposer_agent()
        )

    @task
    def judge_task(self):
        return Task(
            config=self.tasks_config['judge_task'],
            agent=self.judge_agent()
        )

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )