import asyncio
import logging
import time
from typing import Callable, Any, Awaitable


class Cache:
    """缓存管理"""
    def __init__(self):
        # 全局数据锁
        self.__global_lock: dict[str, asyncio.Lock] = {}
        # 全局数据
        self.__global_data = {}

    def __get_lock(self, key: str) -> asyncio.Lock:
        """获取一个全局锁"""
        if key not in self.__global_lock:
            self.__global_lock[key] = asyncio.Lock()
        return self.__global_lock[key]

    async def set_data(self, key: str, value: any):
        """添加全局数据"""
        async with self.__get_lock(key):
            self.__global_data[key] = value

    async def get_data(
        self,
        key: str,
        init: Callable[[], Any] = None,
        async_init: Callable[[], Awaitable[Any]] = None
    ) -> Any:
        """
        获取全局数据
        :param key: 全局key
        :param init: 初始化函数（不存在时调用该方法初始化）
        :param async_init: 异步初始化函数
        :return: 缓存的数据
        """
        async with self.__get_lock(key):
            data = self.__global_data.get(key)
            if data is None:
                start = time.time()
                if async_init is not None:
                    data = await async_init()
                elif init is not None:
                    data = init()
                logging.info(f'get from init, cost {(time.time() - start):.4f}s')
                if data is not None:
                    self.__global_data[key] = data
            else:
                logging.info(f'get from cache')
        return data
