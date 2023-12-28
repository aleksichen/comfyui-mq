import json

from aio_pika import Message
from loguru import logger

from mq.config import paint_progress_config, paint_result_config
from mq.rabbitmq import rabbitmq


@rabbitmq.publisher(paint_progress_config)
async def send_paint_worker_event_progress(user_id: int, prompt_id: int,  progress: float) -> Message:
    """
    发送绘图进度消息
    Args:
        user_id:
        prompt_id:
        progress:

    Returns:

    """
    logger.info(f"send_paint_worker_event_progress: {user_id}, {prompt_id}, {progress}")
    # 构建消息
    payload = {
        "user_id": str(user_id),
        "prompt_id": str(prompt_id),
        "value": str(progress)
    }
    payload_str = json.dumps(payload)

    message = Message(
        body=payload_str.encode(),
    )

    return message


@rabbitmq.publisher(paint_result_config)
async def send_paint_result(user_id: int, prompt_id: int, imgs: []):
    """
    当绘图有了结果后，发送消息给前端
    Args:
        user_id:
        prompt_id:
        imgs:

    Returns:

    """

    logger.info(f"send_paint_result: {user_id}, {prompt_id}, {imgs}")

    # 构建消息
    payload = {
        "user_id": str(user_id),
        "prompt_id": str(prompt_id),
        "value": json.dumps(imgs)
    }

    payload_str = json.dumps(payload)

    message = Message(
        body=payload_str.encode(),
    )

    return message





if __name__ == '__main__':
    import asyncio


    async def main():
        await my_publisher_function.call("")


    asyncio.run(main())
