from crewai import Crew, Task, Agent
from crewai.project import CrewBase, agent, crew, task
from apps.debate.agents.defender import create_defender_agent
from apps.debate.agents.opposer import create_opposer_agent
from apps.debate.agents.judge import create_judge_agent


@CrewBase
class DebateCrew():
    """Optimized debate crew - single execution, controlled communication."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        super().__init__()
        # ✅ Cache agents to prevent redundant instantiation
        self._defender = None
        self._opposer = None
        self._judge = None
    
    # ===== CACHED AGENTS =====
    @agent
    def defender_agent(self) -> Agent:
        if self._defender is None:
            self._defender = create_defender_agent(self.agents_config)
        return self._defender
    
    @agent
    def opposer_agent(self) -> Agent:
        if self._opposer is None:
            self._opposer = create_opposer_agent(self.agents_config)
        return self._opposer
    
    @agent
    def judge_agent(self) -> Agent:
        if self._judge is None:
            self._judge = create_judge_agent(self.agents_config)
        return self._judge
    
    # ===== ROUND 1 =====
    @task
    def defend_round1_task(self) -> Task:
        return Task(
            config=self.tasks_config['defend_task'],
            agent=self.defender_agent()
        )
    
    @task
    def oppose_round1_task(self) -> Task:
        return Task(
            config=self.tasks_config['oppose_task'],
            agent=self.opposer_agent(),
            context=[self.defend_round1_task()]  # ✅ Sees defender's R1 output
        )
    
    # ===== ROUND 2 =====
    @task
    def defend_round2_task(self) -> Task:
        return Task(
            config=self.tasks_config['defend_task'],
            agent=self.defender_agent(),
            context=[self.defend_round1_task(), self.oppose_round1_task()]  # ✅ Sees both R1
        )
    
    @task
    def oppose_round2_task(self) -> Task:
        return Task(
            config=self.tasks_config['oppose_task'],
            agent=self.opposer_agent(),
            context=[self.defend_round1_task(), self.oppose_round1_task(), self.defend_round2_task()]  # ✅ Sees all previous
        )
    
    # ===== JUDGMENT =====
    @task
    def judge_task(self) -> Task:
        return Task(
            config=self.tasks_config['judge_task'],
            agent=self.judge_agent(),
            context=[
                self.defend_round1_task(),
                self.oppose_round1_task(),
                self.defend_round2_task(),
                self.oppose_round2_task()
            ]  # ✅ Judge sees complete debate
        )
    
    # ===== SINGLE CREW =====
    @crew
    def crew(self) -> Crew:
        """
        Single crew that executes entire 2-round debate + judgment.
        ✅ Only 3 agents created (cached)
        ✅ Only 5 LLM calls total
        ✅ Sequential execution prevents resource explosion
        """
        return Crew(
            agents=[
                self.defender_agent(),
                self.opposer_agent(),
                self.judge_agent()
            ],
            tasks=[
                self.defend_round1_task(),
                self.oppose_round1_task(),
                self.defend_round2_task(),
                self.oppose_round2_task(),
                self.judge_task()
            ],
            verbose=True,
            process="sequential"
        )