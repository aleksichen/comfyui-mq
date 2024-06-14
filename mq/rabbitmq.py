import asyncio
import threading

import aio_pika
from typing import List, Tuple, Callable

from loguru import logger
from pydantic import BaseModel

from configs.mq import settings


class MqMessageConfig(BaseModel):
    exchange_name: str = 'default_exchange'
    exchange_type: str = 'direct'
    queue_name: str = 'default_queue'
    routing_key: str = ''
    durable: bool = False
    auto_delete: bool = False


class MyRabbitMQ:
    def __init__(self, url=None, host: str = None, port: int = 5672, username: str = "guest", password: str = "guest"):
        self.url = url
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection: aio_pika.Connection = None
        self.consumers: List[Tuple[Callable, MqMessageConfig]] = []

    def _build_url(self):
        return f"amqp://{self.username}:{self.password}@{self.host}"

    async def connect(self):
        if self.url is None:
            self.url = self._build_url()
        self.connection = await aio_pika.connect_robust(self.url)

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    def consumer(self, mq_message_config: MqMessageConfig):
        def decorator(func: Callable):
            self.consumers.append((func, mq_message_config))
            return func

        return decorator


    async def consuming(self, mq_config: MqMessageConfig, context, func: Callable):
        await self.consume(func, mq_config, context)


    async def consuming_all(self, context):
        for func, mq_config in self.consumers:
            await self.consume(func, mq_config, context)

    async def consume(self, func, mq_config, context):
        logger.info(f"start consuming {func.__name__} with config: {mq_config.dict()}")
        # 1. 获取channel
        channel = await self.connection.channel()
        # 2. 声明 exchange
        exchange = await channel.declare_exchange(mq_config.exchange_name, mq_config.exchange_type)
        # 3. 声明队列
        queue = await channel.declare_queue(mq_config.queue_name, durable=mq_config.durable,
                                            auto_delete=mq_config.auto_delete)
        # 4. 绑定队列
        await queue.bind(exchange=exchange, routing_key=mq_config.routing_key)
        async def on_message(message: aio_pika.IncomingMessage):
            # 调用消费者函数
            await func(message, context)
        # 监听消息
        await queue.consume(on_message)

    async def stop_consuming(self):
        for _, mq_config in self.consumers:
            channel = await self.connection.channel()
            exchange = await channel.declare_exchange(mq_config.exchange_name, mq_config.exchange_type)
            queue = await channel.declare_queue(mq_config.queue_name, durable=mq_config.durable, auto_delete=mq_config.auto_delete)
            await queue.unbind(exchange=exchange, routing_key=mq_config.routing_key)
            await queue.delete()

    def publisher(self, mq_message_config: MqMessageConfig):
        def decorator(func: Callable):
            async def wrapper(*args, **kwargs):
                # 1. 连接到 RabbitMQ
                connection = await aio_pika.connect_robust(self.url)
                # 2. 获取 channel
                channel = await connection.channel()
                # 3. 声明 exchange
                exchange = await channel.declare_exchange(mq_message_config.exchange_name, mq_message_config.exchange_type)
                # 4. 声明队列
                queue = await channel.declare_queue(mq_message_config.queue_name, durable=mq_message_config.durable, auto_delete=mq_message_config.auto_delete)
                # 5. Binding queue
                await queue.bind(exchange, mq_message_config.routing_key)
                # 6. 构建消息体
                message = await func(*args, **kwargs)
                # 7. 发送消息
                logger.info(f"发送消息: {mq_message_config.dict()}")
                await exchange.publish(message, routing_key=mq_message_config.routing_key)
                # 8. 关闭连接
                await connection.close()

            async def call(*args, **kwargs):
                await wrapper(*args, **kwargs)


            def call_sync(*args, **kwargs):
                # 检查是否在主线程中
                if threading.current_thread() is threading.main_thread():
                    # 主线程
                    if asyncio.get_event_loop().is_running():
                        # 如果事件循环已经运行，创建一个新的事件循环
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        try:
                            new_loop.run_until_complete(wrapper(*args, **kwargs))
                        finally:
                            new_loop.close()
                            asyncio.set_event_loop(None)
                    else:
                        # 如果没有运行的事件循环，直接运行
                        asyncio.run(wrapper(*args, **kwargs))
                else:
                    # 子线程
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(wrapper(*args, **kwargs))
                    finally:
                        loop.close()
                        asyncio.set_event_loop(None)

            wrapper.call = call
            wrapper.call_sync = call_sync
            return wrapper

        return decorator



rabbitmq = MyRabbitMQ(url=settings.RABBITMQ_URL)

if __name__ == '__main__':
    pass
