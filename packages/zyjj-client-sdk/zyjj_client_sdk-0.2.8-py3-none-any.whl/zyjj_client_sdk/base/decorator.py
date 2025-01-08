import asyncio
import logging
from functools import wraps


def async_debounce(wait):
    def decorator(func):
        task: asyncio.Task | None = None

        @wraps(func)
        async def debounced(*args, **kwargs):
            nonlocal task

            async def call_func():
                await asyncio.sleep(wait)
                await func(*args, **kwargs)

            if task and not task.done():
                logging.info("[debounce] has task cancel")
                task.cancel()

            task = asyncio.create_task(call_func())
            return await task

        return debounced

    return decorator


def async_throttle(wait: float):
    """
    异步节流器（控制程序在固定时间内只执行一次）
    :param wait:
    :return:
    """
    def decorator(func):
        task: asyncio.Task | None = None

        @wraps(func)
        async def throttle(*args, **kwargs):
            nonlocal task
            if task and not task.done():
                logging.info("[throttle] task unfinished ignore")
                return

            async def call_func():
                await func(*args, **kwargs)
                await asyncio.sleep(wait)

            task = asyncio.create_task(call_func())
            return await task

        return throttle

    return decorator
