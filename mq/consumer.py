import json
import uuid

from loguru import logger

import execution
from mq.config import paint_server_event_config
from mq.rabbitmq import rabbitmq


@rabbitmq.consumer(paint_server_event_config)
async def on_paint_event(message, context):
    """
    当收到绘图任务后，将任务转成q，然后提交到q
    """
    async with message.process():
        logger.info(f"接收到fastapi的绘图任务: {message.body.decode()}")

        payload = json.loads(message.body.decode())
        user_id = payload.get("user_id")
        prompt_id = payload.get("prompt_id")
        prompt = payload.get("prompt")

        q = context.get("q")

        valid = execution.validate_prompt(prompt)
        outputs_to_execute = valid[2]
        number = 1
        extra_data = {
            "client_id": user_id,
        }
        q.put((number, prompt_id, prompt, extra_data, outputs_to_execute))
        response = {"prompt_id": prompt_id, "number": number, "node_errors": valid[3]}
        logger.info(f"response: {response}")

