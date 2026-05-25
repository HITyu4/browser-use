"""
Browser Use Demo Mode Test - Using DeepSeek Model

Prerequisites:
1. Set DEEPSEEK_API_KEY=sk-your-key in .env

Run:
    cd /Users/hityu/PyCharmMiscProject/browser-use
    uv run python examples/deepseek_demo_test.py
"""

import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, BrowserProfile
from browser_use.llm import ChatDeepSeek

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
	logger.info('Starting DeepSeek browser use demo')
	api_key = os.getenv('DEEPSEEK_API_KEY')
	base_url = 'https://api.deepseek.com/v1'

	if not api_key:
		raise ValueError('Please set DEEPSEEK_API_KEY in .env file')

	llm = ChatDeepSeek(
		model='deepseek-chat',
		api_key=api_key,
		base_url=base_url,
	)
	logger.info('DeepSeek model configured')

	browser_profile = BrowserProfile(enable_default_extensions=False)
	browser = Browser(browser_profile=browser_profile)
	logger.info('Browser created (extensions disabled)')

	agent = Agent(
		task='帮我在bilibili搜索有关agent的视频',
		llm=llm,
		browser=browser,
		use_vision=True,
		max_actions_per_step=2,
		demo_mode=True,
	)
	logger.info('Agent created, starting run')

	result = await agent.run(max_steps=20)
	logger.info('Agent run completed with result: %s', result)


if __name__ == '__main__':
	asyncio.run(main())
