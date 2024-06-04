from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from agentops.agent import track_agent
import os


@CrewBase
class StartUp_Researcher_Crew:
    """Start-Up researcher crew for analyzing and researching on the startup ideas."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        # Groq
        self.groq_llm = ChatGroq(
            temperature=0,
            groq_api_key="GROQ API KEY",
            model_name="llama3-70b-8192" #"llama3-70b-8192",
        )
    
    @track_agent(name="marketer")
    @agent
    def marketer(self) -> Agent:
        return Agent(
            config=self.agents_config["marketer"],
            allow_delegation=False,
            llm=self.groq_llm,
            verbose=True,
        )
    
    @track_agent(name="technologist")
    @agent
    def technologist(self) -> Agent:
        return Agent(
            config=self.agents_config["technologist"],
            allow_delegation=False,
            llm=self.groq_llm,
            verbose=True,
        )
    
    @track_agent(name="business_consultant")
    @agent
    def business_consultant(self) -> Agent:
        return Agent(
            config=self.agents_config["business_consultant"],
            allow_delegation=False,
            llm=self.groq_llm,
            verbose=True,
        )
        
    @task
    def marketer_task(self) -> Task:
        return Task(
            config=self.tasks_config["marketer"],
            agent=self.marketer(),
            human_input=True,
            output_file="marketer.md",
        )
    
    @task
    def technologist_task(self) -> Task:
        return Task(
            config=self.tasks_config["technologist"],
            agent=self.technologist(),
            output_file="technologist.md",
        )
    
    @task
    def business_consultant_task(self) -> Task:
        return Task(
            config=self.tasks_config["business_consultant"],
            agent=self.business_consultant(),
            output_file="startup_research.md",
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.marketer(),
                self.technologist(),
                self.business_consultant(),
            ],
            tasks=[
                self.marketer_task(),
                self.technologist_task(),
                self.business_consultant_task(),
            ],
            process = Process.sequential,
            memory = False,
            max_rpm = 2,
            verbose = 2,
        )
