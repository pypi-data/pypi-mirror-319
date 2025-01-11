from agents4sky import CodeAgent, DuckDuckGoSearchTool, HfApiModel, tool
from dotenv import load_dotenv
import unittest
from typing import Dict, List
from datetime import datetime
import json

# 加载环境变量
load_dotenv()

@tool
def search_drone_info(query: str) -> str:
    """Search for drone-related information using DuckDuckGo.

    Args:
        query: The specific search query about drone logistics, delivery, or operations.
               For example: "best drones for urban delivery" or "drone regulations in Shanghai".

    Returns:
        str: Search results containing relevant drone information.
    """
    search_tool = DuckDuckGoSearchTool()
    return search_tool(query)

@tool
def format_response(response: Dict) -> str:
    """Format dictionary response into a readable string.

    Args:
        response: Dictionary containing response data to be formatted.

    Returns:
        str: Formatted string representation of the response.
    """
    if isinstance(response, dict):
        return json.dumps(response, indent=2)
    return str(response)


class TestLogisticsSystem(unittest.TestCase):
    def setUp(self):
        # 初始化 agents，添加格式化工具
        self.drone_agent = CodeAgent(
            tools=[DuckDuckGoSearchTool(), search_drone_info, format_response],
            model=HfApiModel()
        )
        
        self.regulatory_agent = CodeAgent(
            tools=[DuckDuckGoSearchTool(), search_drone_info, format_response],
            model=HfApiModel()
        )

    def test_basic_delivery_planning(self):
        """测试基本配送规划流程"""
        try:
            # 1. 监管检查
            regulatory_query = """
            Research drone delivery regulations for Shanghai and format the response as a string.
            Follow these steps:
            1. Search for regulations
            2. Format the findings into a clear text response
            3. Include key points about:
               - Required permits
               - Flight restrictions
            """
            regulatory_response = self.regulatory_agent.run(regulatory_query)
            print("\nRegulatory Analysis:", regulatory_response)
            
            # 验证响应类型
            self.assertIsInstance(regulatory_response, str)
            self.assertTrue(len(regulatory_response) > 0)
            
            # 2. 无人机信息搜索
            drone_query = """
            Search for suitable delivery drones for urban operations in Shanghai.
            Format the response as a clear text summary including:
            - Recommended drone models
            - Key specifications
            - Compliance with local regulations
            """
            drone_response = self.drone_agent.run(drone_query)
            print("\nDrone Research:", drone_response)
            
            # 验证响应类型
            self.assertIsInstance(drone_response, str)
            self.assertTrue(len(drone_response) > 0)

        except Exception as e:
            self.fail(f"Test failed with error: {str(e)}")

    def validate_response(self, response) -> str:
        """验证并格式化响应"""
        if isinstance(response, dict):
            return json.dumps(response, indent=2)
        return str(response)


if __name__ == '__main__':
    unittest.main(verbosity=2)