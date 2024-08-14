from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.rss_tool import RSSFeedTool
from tools.get_content import GetWebsiteContent
from langchain.chat_models.openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

defalut_llm = ChatOpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"),
                        temperature=0.1,                        
                        model_name="gpt-4o-mini")

@CrewBase
class NewsletterAgentsCrew():
	"""NewsletterAgents crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def rss_feed_consumer(self) -> Agent:
		return Agent(
			config=self.agents_config['rss_feed_consumer'],
			verbose=True,
			llm=defalut_llm,
			allow_delegation=False,
			tools=[RSSFeedTool()],
			max_iter=30
		)
	
	@agent
	def content_extractor(self) -> Agent:
		return Agent(
			config=self.agents_config['content_extractor'],
			verbose=True,
			llm=defalut_llm,
			allow_delegation=False,
			tools=[GetWebsiteContent()],
			max_iter=20
		)

	@agent
	def article_curator(self) -> Agent:
		return Agent(
			config=self.agents_config['article_curator'],
			verbose=True,
			llm=defalut_llm,
			allow_delegation=False,
			max_iter=5
			
		)

	@task
	def consume_rss_feed(self) -> Task:
		return Task(
			config=self.tasks_config['consume_rss_feed'],
			agent=self.rss_feed_consumer()
		)
	
	@task
	def extract_content_summary(self) -> Task:
		return Task(
			config=self.tasks_config['extract_content_summary'],
			agent=self.content_extractor()
		)
	
	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['curate_articles'],
			agent=self.article_curator()
		)
	
	@task
	def improve_newsletter_based_on_critique(self) -> Task:

		reporting_task = self.reporting_task()
		extract_content_summary = self.extract_content_summary()
	
		return Task(
			config=self.tasks_config['improve_newsletter_based_on_critique'],
			agent=self.article_curator(),
			context=[extract_content_summary, reporting_task],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the NewsletterAgents crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2
		)