from agents4sky import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from dotenv import load_dotenv

load_dotenv()

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

agent.run("在重庆市那个区县发展低空经济最有机会")
 