from agents4sky.default_tools import (
    PythonInterpreterTool,
    FinalAnswerTool,
    DuckDuckGoSearchTool,
    VisitWebpageTool
)
import unittest
from dotenv import load_dotenv
import time

# 加载环境变量
load_dotenv()

class TestDefaultTools(unittest.TestCase):
    def setUp(self):
        """初始化所有工具"""
        self.python_tool = PythonInterpreterTool()
        self.final_answer_tool = FinalAnswerTool()
        self.ddg_search_tool = DuckDuckGoSearchTool()
        self.webpage_tool = VisitWebpageTool()

    def test_python_calculator(self):
        """测试 Python 计算器功能"""
        print("\n=== Testing Python Calculator ===")
        
        code = """
import math

def calculate_circle_area(radius):
    return math.pi * radius ** 2

# 计算半径为5的圆的面积
radius = 5
area = calculate_circle_area(radius)
print(f"圆的面积是: {area:.2f}")

# 计算一些基础数学
print(f"2 + 2 = {2 + 2}")
print(f"10 * 5 = {10 * 5}")
print(f"100 / 4 = {100 / 4}")
"""
        result = self.python_tool.forward(code)
        print(result)
        self.assertIn("圆的面积", result)

    def test_web_search(self):
        """测试网络搜索功能"""
        print("\n=== Testing Web Search ===")
        
        print("\nTesting DuckDuckGo Search...")
        query = "Python programming language latest version"
        result = self.ddg_search_tool.forward(query)
        print(f"DuckDuckGo Search Results for '{query}':")
        print(result)
        self.assertIn("Search Results", result)
        
        time.sleep(2)

    def test_webpage_reader(self):
        """测试网页阅读功能"""
        print("\n=== Testing Webpage Reader ===")
        
        # 测试 Python 官网
        url = "https://python.org"
        print(f"\nReading webpage: {url}")
        result = self.webpage_tool.forward(url)
        print(f"First 500 characters of content:\n{result[:500]}...")
        self.assertGreater(len(result), 0)

    def test_final_answer(self):
        """测试最终答案工具"""
        print("\n=== Testing Final Answer Tool ===")
        
        test_cases = [
            "This is a simple string answer",
            {"key": "value", "data": "test"},
            ["item1", "item2"],
            123,
            3.14
        ]
        
        for test_case in test_cases:
            print(f"\nTesting with input: {test_case}")
            result = self.final_answer_tool.forward(test_case)
            print(f"Result: {result}")
            self.assertEqual(result, test_case)

    def test_combined_tools(self):
        """测试工具组合使用"""
        print("\n=== Testing Combined Tools Usage ===")
        
        # 1. 搜索 Python 版本信息
        search_query = "Python latest version features"
        search_results = self.ddg_search_tool.forward(search_query)
        print("\nSearch Results:")
        print(search_results)
        
        time.sleep(2)
        
        # 2. 使用 Python 处理搜索结果
        python_code = f'''
# 分析搜索结果中的版本号
import re

search_text = """{search_results}"""
version_pattern = r'Python \d+\.\d+'
found_versions = re.findall(version_pattern, search_text)

if found_versions:
    print("Found Python versions:", set(found_versions))
else:
    print("No Python versions found in the search results")
'''
        process_result = self.python_tool.forward(python_code)
        print("\nProcessed Results:")
        print(process_result)
        
        # 3. 生成最终答案
        final_result = self.final_answer_tool.forward({
            "search_results_summary": search_results[:200] + "...",
            "version_analysis": process_result
        })
        print("\nFinal Answer:")
        print(final_result)
        
        self.assertIsNotNone(final_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)