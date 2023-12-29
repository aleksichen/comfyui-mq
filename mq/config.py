
from mq.rabbitmq import MqMessageConfig

# fastapi给worker发送消息
paint_server_event_config = MqMessageConfig(
    exchange_name="paint_server_exchange",
    queue_name="paint_server_event_queue",
    routing_key="paint_server_event_queue_key",
)

# worker给fastapi发送开始消息
paint_worker_started_config = MqMessageConfig(
    exchange_name="paint_worker_exchange",
    queue_name="paint_lifecycle_queue",
    routing_key="paint_lifecycle_queue_key",
)

# worker给fastapi发送进度消息
paint_worker_progress_config = MqMessageConfig(
    exchange_name="paint_worker_exchange",
    queue_name="paint_progress_queue",
    routing_key="paint_progress_queue_key",
)

# worker给fastapi发送结果消息
paint_worker_result_config = MqMessageConfig(
    exchange_name="paint_worker_exchange",
    queue_name="paint_worker_result_queue",
    routing_key="paint_worker_result_queue_key",
)
