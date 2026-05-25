"""
Browser Use 执行过程详解 - 带详细日志输出

基于 deepseek_example.py，捕获每个 step 的上下文和动作
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info('=' * 60)
    logger.info('开始 DeepSeek browser use 执行过程详解')
    logger.info('=' * 60)

    api_key = os.getenv('DEEPSEEK_API_KEY')
    base_url = 'https://api.deepseek.com/v1'

    if not api_key:
        raise ValueError('请设置 DEEPSEEK_API_KEY in .env file')

    llm = ChatDeepSeek(
        model='deepseek-chat',
        api_key=api_key,
        base_url=base_url,
    )
    logger.info('LLM: DeepSeek model configured')

    browser_profile = BrowserProfile(enable_default_extensions=False)
    browser = Browser(browser_profile=browser_profile)
    logger.info('Browser: Chrome created (extensions disabled)')

    agent = Agent(
        task='Browse baidu and find any introduction videos about browser use agents',
        llm=llm,
        browser=browser,
        use_vision=True,
        max_actions_per_step=1,
        demo_mode=True,
    )
    logger.info('Agent: Created with task="Browse baidu and find any introduction videos about browser use agents"')
    logger.info('Agent: use_vision=True, max_actions_per_step=1, demo_mode=True')
    logger.info('=' * 60)
    logger.info('开始执行 agent.run(max_steps=10)')
    logger.info('=' * 60)

    result = await agent.run(max_steps=10)

    logger.info('=' * 60)
    logger.info('执行完成，打印完整结果')
    logger.info('=' * 60)

    # 打印每一步的执行详情
    if hasattr(result, 'steps') and result.steps:
        for i, step in enumerate(result.steps):
            logger.info('-' * 40)
            logger.info(f'Step {i + 1} / {len(result.steps)}')
            logger.info('-' * 40)

            # 打印 LLM 返回的动作
            logger.info('【LLM 返回的动作】')
            if hasattr(step, 'actions') and step.actions:
                for j, action in enumerate(step.actions):
                    logger.info(f'  Action {j + 1}: {action.name}')
                    if hasattr(action, 'params') and action.params:
                        params_str = ', '.join([f'{k}={v}' for k, v in action.params.items()])
                        logger.info(f'    Params: {params_str}')
            else:
                logger.info('  (无动作)')

            # 打印执行结果
            logger.info('【动作执行结果】')
            if hasattr(step, 'result') and step.result:
                for j, res in enumerate(step.result):
                    success_str = '成功' if res.success else '失败'
                    logger.info(f'  Result {j + 1}: {success_str}')
                    if res.extracted_content:
                        content_preview = str(res.extracted_content)[:200]
                        logger.info(f'    Content: {content_preview}...')
                    if res.error:
                        logger.info(f'    Error: {res.error}')
            else:
                logger.info('  (无结果)')

            # 打印状态信息
            if hasattr(step, 'state') and step.state:
                logger.info('【当前状态】')
                if hasattr(step.state, 'url'):
                    logger.info(f'  URL: {step.state.url}')
                if hasattr(step.state, 'title'):
                    logger.info(f'  Title: {step.state.title}')

    # 打印最终结果
    logger.info('=' * 60)
    logger.info('最终结果 (final_result)')
    logger.info('=' * 60)
    final = result.final_result() if hasattr(result, 'final_result') else str(result)
    logger.info(final[:500] if len(str(final)) > 500 else final)

    logger.info('=' * 60)
    logger.info('执行过程详解结束')
    logger.info('=' * 60)


if __name__ == '__main__':
    asyncio.run(main())
