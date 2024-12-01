from aiokafka import AIOKafkaConsumer
import asyncio
import logging

logger = logging.getLogger(__name__)

'''
    Это только заготовка, пока ничего с кафкой не коннектил
'''

class KafkaConsumerService:
    def __init__(self, topic: str, bootstrap_servers: str):
        logger.info('Kafka init')
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id="my_group_id"
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer connected to topic: {self.topic}")

    async def consume(self):
        try:
            async for message in self.consumer:
                logger.info(f"Got message: {message.value.decode('utf-8')}")
        except Exception as e:
            logger.error("Got error from Kafka: ", e)
        finally:
            await self.consumer.stop()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
