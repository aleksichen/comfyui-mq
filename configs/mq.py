import os

class Settings:
    # mq
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "101.33.201.174")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
    RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "snowycat")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "20230925_kns")
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/?heartbeat=600")

settings = Settings()



if __name__ == "__main__":
    print(settings.RABBITMQ_URL)