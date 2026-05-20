"""
Browser Use Demo Mode Test - Using Qwen Model

Prerequisites:
1. Set ALIBABA_CLOUD=sk-your-qwen-key in .env
2. Set BROWSER_USE_API_KEY=bu-your-key in .env (optional, for cloud features)

Run:
    uv run python examples/qwen_demo_test.py
"""

import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, BrowserProfile, ChatOpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
	logger.info('Starting Qwen browser use demo')
	api_key = os.getenv('ALIBABA_CLOUD')
	base_url = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'

	llm = ChatOpenAI(
		model='qwen-vl-max',
		api_key=api_key,
		base_url=base_url,
	)
	logger.info('Qwen model configured')

	browser_profile = BrowserProfile(enable_default_extensions=False)
	browser = Browser(browser_profile=browser_profile)
	logger.info('Browser created (extensions disabled)')

	agent = Agent(
		task='Open https://www.baidu.com and tell me the title of this page',
		llm=llm,
		browser=browser,
		use_vision=True,
		max_actions_per_step=1,
		demo_mode=True,
	)
	logger.info('Agent created, starting run')

	result = await agent.run(max_steps=10)
	logger.info('Agent run completed with result: %s', result)


if __name__ == '__main__':
	asyncio.run(main())
