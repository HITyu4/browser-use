"""
Browser Use Cloud Stealth Browser Test

Uses Browser Use Cloud's stealth browser with the following features:
- Anti-detection (websites cannot identify automation)
- Automatic proxy rotation
- Avoids CAPTCHA

Prerequisites:
1. Set BROWSER_USE_API_KEY=bu_xxx in .env

Run:
    cd /Users/hityu/PyCharmMiscProject/browser-use
    uv run python examples/cloud_browser_test.py
"""

import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser
from browser_use.llm import ChatDeepSeek

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
	logger.info('Starting cloud stealth browser demo')
	api_key = os.getenv('DEEPSEEK_API_KEY')
	if not api_key:
		raise ValueError('Please set DEEPSEEK_API_KEY in .env file')

	llm = ChatDeepSeek(
		model='deepseek-chat',
		api_key=api_key,
		base_url='https://api.deepseek.com/v1',
	)
	logger.info('DeepSeek model configured')

	browser = Browser(use_cloud=True)
	logger.info('Cloud stealth browser created')

	agent = Agent(
		task='Browse YouTube and find any introduction videos about browser use agents',
		llm=llm,
		browser=browser,
		demo_mode=True,
	)
	logger.info('Agent created, starting run')

	result = await agent.run(max_steps=10)
	logger.info('Agent run completed with result: %s', result)


if __name__ == '__main__':
	asyncio.run(main())
