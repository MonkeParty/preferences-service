from aiokafka import AIOKafkaConsumer
from config import settings
import asyncio
import logging
import model
import json
import requests

logger = logging.getLogger(__name__)

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
            group_id=settings.KAFKA_GROUP_ID
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer connected to topic: {self.topic}")

    def get_movie_info(movie_id : int) -> model.MovieInfo:
        # don't forget add movie_id to request ?? нету спеки бля
        movieResponse = requests.get(settings.MOVIE_SERVICE_HOST)
        if movieResponse.status_code != 200:
            raise Exception("Something wrong")
        json_result = movieResponse.json()
        return model.MovieInfo(movie_id=json_result['movie_id'], 
                            genre=json_result['genre'], 
                            avg_rate=json_result['avg_rate'])

    async def processing(message : bytes):
        logger.info(f"Got message from kafka: {message.value.decode('utf-8')}")
        action_request = None
        try:
            data = json.loads(message.value.decode('utf-8'))
            action_request = model.ActionRequest(**data)
            logger.info(f"Processed ActionRequest: {action_request}")
        except Exception as e:
            logger.error(f"Failed to decode JSON: {e}")
            return None
        
        # работаем с action_request
        # тут обработка, вычисление весов и всего такого
        # и обновление данных в БД
        pass

    async def consume(self):
        try:
            async for message in self.consumer:
                await self.processing(message)
        except Exception as e:
            logger.error("Got error from Kafka: ", e)
        finally:
            await self.consumer.stop()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
