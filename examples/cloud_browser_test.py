"""
Browser Use 云端 Stealth 浏览器测试

使用 Browser Use Cloud 的 stealth 浏览器，功能：
- 反检测（网站无法识别自动化）
- 自动代理轮换
- 避免 CAPTCHA

前提条件：
1. 在 .env 中配置 BROWSER_USE_API_KEY=bu_xxx

运行方式：
    cd /Users/hityu/PyCharmMiscProject/browser-use
    uv run python examples/cloud_browser_test.py
"""

import asyncio
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser
from browser_use.llm import ChatDeepSeek


async def main() -> None:
	# 使用自己的 DeepSeek 模型
	api_key = os.getenv('DEEPSEEK_API_KEY')
	if not api_key:
		raise ValueError('请在 .env 中配置 DEEPSEEK_API_KEY')

	llm = ChatDeepSeek(
		model='deepseek-chat',
		api_key=api_key,
		base_url='https://api.deepseek.com/v1',
	)

	# 创建云端 stealth 浏览器
	browser = Browser(use_cloud=True)

	# 创建 Agent
	agent = Agent(
		task='看看youtube网站有没有agent相关介绍视频',
		llm=llm,
		browser=browser,
		demo_mode=True,
	)

	# 运行 agent
	result = await agent.run(max_steps=10)
	print(f'\n执行结果: {result}')


if __name__ == '__main__':
	asyncio.run(main())