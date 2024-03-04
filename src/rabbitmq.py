from aio_pika import Message, connect

from config import settings


class RabbitMQ:
    def __init__(self):
        self.address = (
            f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@localhost/"
        )

    async def __aenter__(self):
        self.connection = await connect(self.address)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    async def publish(self, message: str, routing_key: str):
        channel = await self.connection.channel()
        await channel.default_exchange.publish(
            Message(message.encode("utf-8")), routing_key=routing_key
        )


rabbit = RabbitMQ()
