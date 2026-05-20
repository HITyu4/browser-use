"""
Browser Use Demo Mode 测试 - 使用 Qwen 模型

前提条件：
1. 在 .env 中配置 ALIBABA_CLOUD=sk-your-qwen-key
2. 在 .env 中配置 BROWSER_USE_API_KEY=bu-your-key（可选，用于云端功能）

运行方式：
    uv run python examples/qwen_demo_test.py
"""

import asyncio
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, BrowserProfile, ChatOpenAI


async def main() -> None:
	# 配置 Qwen 模型
	api_key = os.getenv('ALIBABA_CLOUD')
	base_url = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'

	llm = ChatOpenAI(
		model='qwen-vl-max',
		api_key=api_key,
		base_url=base_url,
	)

	# 创建浏览器配置，禁用扩展（避免下载失败）
	browser_profile = BrowserProfile(enable_default_extensions=False)

	# 创建浏览器实例
	browser = Browser(browser_profile=browser_profile)

	# 创建 Agent，启用 demo_mode
	agent = Agent(
		task='请打开 https://www.baidu.com 并告诉我这个页面的标题是什么',
		llm=llm,
		browser=browser,
		use_vision=True,  # Qwen 需要启用视觉能力
		max_actions_per_step=1,  # 每步只执行一个动作
		demo_mode=True,  # 启用演示模式，可以看到决策过程
	)

	# 运行 agent
	result = await agent.run(max_steps=10)
	print(f"\n执行结果: {result}")


if __name__ == '__main__':
	asyncio.run(main())