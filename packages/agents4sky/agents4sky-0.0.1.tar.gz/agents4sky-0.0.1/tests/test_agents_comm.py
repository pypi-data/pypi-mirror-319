from agents4sky import CodeAgent, ManagedAgent, DuckDuckGoSearchTool, HfApiModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建子 agent
search_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel()
)

# 创建被管理的 agent
managed_search_agent = ManagedAgent(
    agent=search_agent,
    name="search_expert",
    description="An expert at searching information",
    provide_run_summary=True  # 这样可以获取子 agent 的执行过程
)

# 创建主 agent
main_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel(),
    managed_agents=[managed_search_agent]  # 添加被管理的 agent
)

# 主 agent 可以调用子 agent
result = main_agent.run("Find information about Python and process it")

