
from mq.rabbitmq import MqMessageConfig

paint_event_config = MqMessageConfig(
    exchange_name="paint_exchange",
    queue_name="paint_event_queue",
    routing_key="paint_event_queue_key",
)
