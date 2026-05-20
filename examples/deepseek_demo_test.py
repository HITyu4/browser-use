"""
Browser Use Demo Mode 测试 - 使用 DeepSeek 模型

前提条件：
1. 在 .env 中配置 DEEPSEEK_API_KEY=sk-your-key

运行方式：
    cd /Users/hityu/PyCharmMiscProject/browser-use
    uv run python examples/deepseek_demo_test.py
"""

import asyncio
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, BrowserProfile
from browser_use.llm import ChatDeepSeek


async def main() -> None:
	# 配置 DeepSeek 模型
	api_key = os.getenv('DEEPSEEK_API_KEY')
	base_url = 'https://api.deepseek.com/v1'

	if not api_key:
		raise ValueError('请在 .env 文件中配置 DEEPSEEK_API_KEY')

	llm = ChatDeepSeek(
		model='deepseek-chat',
		api_key=api_key,
		base_url=base_url,
	)

	# 创建浏览器配置，禁用扩展（避免下载失败）
	browser_profile = BrowserProfile(enable_default_extensions=False)

	# 创建浏览器实例
	browser = Browser(browser_profile=browser_profile)

	# 创建 Agent，启用 demo_mode
	agent = Agent(
		task='看看youtube网站有没有agent相关介绍视频',
		llm=llm,
		browser=browser,
		use_vision=True,
		max_actions_per_step=1,
		demo_mode=True,
	)

	# 运行 agent
	result = await agent.run(max_steps=10)
	print(f'\n执行结果: {result}')


if __name__ == '__main__':
	asyncio.run(main())
