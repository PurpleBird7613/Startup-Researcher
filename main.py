from crew import StartUp_Researcher_Crew
from dotenv import load_dotenv
import agentops

load_dotenv()
agentops.init()


def run():
    my_idea = input("Enter your idea: ")
    
    inputs = {"my_idea": my_idea}
    
    crew = StartUp_Researcher_Crew()
    result = crew.crew().kickoff(inputs=inputs)
    
    print(result)
    

if __name__ == "__main__":
    run()