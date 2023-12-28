import json
import uuid

from loguru import logger

import execution
from mq.config import paint_event_config
from mq.rabbitmq import rabbitmq


@rabbitmq.consumer(paint_event_config)
async def on_paint_event(message, context):
    """
    当收到绘图任务后， 将任务转成q， 然后提交到q
    """
    async with message.process():
        logger.info(f"接收到fastapi的绘图任务: {message.body.decode()}")

        payload = json.loads(message.body.decode())
        user_id = payload.get("user_id")
        prompt_config = payload.get("prompt_config")

        q = context.get("q")

        prompt_id = str(uuid.uuid4())
        prompt_config = json.loads(prompt_config)
        prompt = prompt_config.get("prompt")
        valid = execution.validate_prompt(prompt)
        outputs_to_execute = valid[2]
        number = 1
        extra_data = {
            "client_id": user_id,
        }
        q.put((number, prompt_id, prompt, extra_data, outputs_to_execute))
        response = {"prompt_id": prompt_id, "number": number, "node_errors": valid[3]}
        logger.info(f"response: {response}")

