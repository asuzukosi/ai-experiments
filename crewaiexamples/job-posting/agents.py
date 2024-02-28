from crewai import Agent
from crewai_tools.tools import WebsiteSearchTool, SeperDevTool, FileReadTool

# define tools to be used by agents in the crew
# website search tool for searching information on the content provided on a website
web_search_tool = WebsiteSearchTool()
# uses seper to get search results
seper_dev_tool = SeperDevTool()
# uses this tool to read a file to extracti information
file_read_tool = FileReadTool(
	file_path='job_description_example.md',
	description='A tool to read the job description example file.'
)


# define agents to be used in the crew
class Agents():
    # we can se that within this agents we can define the agents we would want to use
    # research agent has 2 search tools
	def research_agent(self):
		return Agent(
			role='Research Analyst',
			goal='Analyze the company website and provided description to extract insights on culture, values, and specific needs.',
			tools=[web_search_tool, seper_dev_tool],
			backstory='Expert in analyzing company cultures and identifying key values and needs from various sources, including websites and brief descriptions.',
			verbose=True
		)
	# writer agent writes insightful job posting, it has access to 3 tools, tools for job posting and reading from a file
	def writer_agent(self):
			return Agent(
				role='Job Description Writer',
				goal='Use insights from the Research Analyst to create a detailed, engaging, and enticing job posting.',
				tools=[web_search_tool, seper_dev_tool, file_read_tool],
				backstory='Skilled in crafting compelling job descriptions that resonate with the company\'s values and attract the right candidates.',
				verbose=True
			)
	# review agent can review the provided job posting and suggest changes
	def review_agent(self):
			return Agent(
				role='Review and Editing Specialist',
				goal='Review the job posting for clarity, engagement, grammatical accuracy, and alignment with company values and refine it to ensure perfection.',
				tools=[web_search_tool, seper_dev_tool, file_read_tool],
				backstory='A meticulous editor with an eye for detail, ensuring every piece of content is clear, engaging, and grammatically perfect.',
				verbose=True
			)
