from dotenv import load_dotenv
load_dotenv()

from crewai import Crew

from tasks import Tasks
from agents import Agents

import openai

openai.base_url = "https://api.openai.com/v1"

# get all the tasks and all the agents
tasks = Tasks() # 5 tasks
agents = Agents() # 3 agents

# specifiy company description and domain
company_description = "We are a shoe making company"
# input("What is the company description?\n")
company_domain = "We make designer shoes"
# input("What is the company domain?\n")
# specify hiring needs and special benefits
hiring_needs = "Shoe making experience"
# input("What are the hiring needs?\n")
specific_benefits = "Remote work"
# input("What are specific_benefits you offer?\n")

# Create Agents
researcher_agent = agents.research_agent()
writer_agent = agents.writer_agent()
review_agent = agents.review_agent()

# Define Tasks for each agent
research_company_culture_task = tasks.research_company_culture_task(researcher_agent, company_description, company_domain)
industry_analysis_task = tasks.industry_analysis_task(researcher_agent, company_domain, company_description)
research_role_requirements_task = tasks.research_role_requirements_task(researcher_agent, hiring_needs)
draft_job_posting_task = tasks.draft_job_posting_task(writer_agent, company_description, hiring_needs, specific_benefits)
review_and_edit_job_posting_task = tasks.review_and_edit_job_posting_task(review_agent, hiring_needs)

# Instantiate the crew with a sequential process
crew = Crew(
    agents=[researcher_agent, writer_agent, review_agent],
    tasks=[
        research_company_culture_task,
        industry_analysis_task,
        research_role_requirements_task,
        draft_job_posting_task,
        review_and_edit_job_posting_task
    ]
)

# Kick off the process
result = crew.kickoff()

print("Job Posting Creation Process Completed.")
print("Final Job Posting:")
print(result)