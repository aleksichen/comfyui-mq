
from mq.rabbitmq import MqMessageConfig

paint_event_config = MqMessageConfig(
    exchange_name="paint_exchange",
    queue_name="paint_event_queue",
    routing_key="paint_event_queue_key",
)

paint_progress_config = MqMessageConfig(
    exchange_name="paint_exchange",
    queue_name="paint_progress_queue",
    routing_key="paint_progress_queue_key",
)

paint_result_config = MqMessageConfig(
    exchange_name="paint_exchange",
    queue_name="paint_result_queue",
    routing_key="paint_result_queue_key",
)