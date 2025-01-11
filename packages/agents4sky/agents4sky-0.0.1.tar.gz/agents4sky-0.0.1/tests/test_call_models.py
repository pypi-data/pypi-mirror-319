from agents4sky import CodeAgent, DuckDuckGoSearchTool
from agents4sky.models import (
    HfApiModel,      # Hugging Face API 模型
    TransformersModel,  # 本地 Transformers 模型
    LiteLLMModel    # 通用 LLM API 模型(支持 OpenAI, Anthropic 等)
)
import os
from dotenv import load_dotenv

load_dotenv()

# 1. 使用 Hugging Face API 模型
hf_model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",  # 默认模型
    token=os.getenv("HF_API_KEY"),  # 或使用环境变量 HF_TOKEN
    timeout=120
)

agent_with_hf = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=hf_model
)

# 2. 使用本地 Transformers 模型
local_model = TransformersModel(
    model_id="HuggingFaceTB/SmolLM2-1.7B-Instruct"  # 默认使用这个小模型
)

agent_with_local = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=local_model
)

# 3. 使用 LiteLLM 支持的各种模型

# 3.2 使用 GPT-4
gpt4_model = LiteLLMModel(
    model_id="gpt-4-turbo-preview",
    api_key=os.getenv("OPENAI_API_KEY")
)
    
# 创建一个支持动态切换模型的 Agent 类
class MultiModelAgent(CodeAgent):
    def switch_model(self, model_type: str, **model_kwargs):
        """动态切换模型"""
        model_map = {
            "hf": lambda: HfApiModel(**model_kwargs),
            "local": lambda: TransformersModel(**model_kwargs),
            "gpt4": lambda: LiteLLMModel(
                model_id="gpt-4-turbo-preview",
                **model_kwargs
            )
        }
        
        if model_type not in model_map:
            raise ValueError(f"Unsupported model type: {model_type}")
            
        self.model = model_map[model_type]()
        # 重置状态
        self.state = {}
        self.logs = []

# 使用示例
agent = MultiModelAgent(
    tools=[DuckDuckGoSearchTool()],
    model=hf_model  # 初始使用 HF 模型
)

# 切换到不同模型
agent.switch_model("claude", api_key="your_anthropic_key")
agent.switch_model("gpt4", api_key="your_openai_key")
agent.switch_model("local", model_id="facebook/opt-350m")  # 使用较小的本地模型

# 根据任务类型自动选择模型
class TaskSpecificAgent(MultiModelAgent):
    def run(self, task: str, **kwargs):
        # 基于任务特征选择模型
        if "code" in task.lower():
            self.switch_model("hf", model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
        elif "math" in task.lower():
            self.switch_model("gpt4", api_key="your_openai_key")
        elif "creative" in task.lower():
            self.switch_model("claude", api_key="your_anthropic_key")
        else:
            self.switch_model("local")  # 默认使用本地模型
            
        return super().run(task, **kwargs)

# 使用特定任务的 agent
task_agent = TaskSpecificAgent(
    tools=[DuckDuckGoSearchTool()],
    model=hf_model
)

# 测试不同任务
task_agent.run("Write a Python function to sort a list")  # 使用 Qwen
task_agent.run("Solve this complex math equation")  # 使用 GPT-4
task_agent.run("Write a creative story")  # 使用 Claude
task_agent.run("Simple task")  # 使用本地模型