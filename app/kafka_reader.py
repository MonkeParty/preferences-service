from aiokafka import AIOKafkaConsumer
from app.config import settings
import asyncio
import logging
import app.model as model
import json
import requests
from app.crud import update_user_info, get_user_info, create_user_info

logger = logging.getLogger(__name__)

class KafkaConsumerService:
    def __init__(self, topic: str, bootstrap_servers: str, get_db):
        logger.info('Kafka init')
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.consumer = None
        self.get_db = get_db

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=settings.KAFKA_GROUP_ID
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer connected to topic: {self.topic}")

    async def processing(self, message : bytes):
        logger.info(f"Got message from kafka: {message.value.decode('utf-8')}")
        action_request = None
        try:
            data = json.loads(message.value.decode('utf-8'))
            action_request = model.ActionRequest(**data)
            logger.info(f"Processed ActionRequest: {action_request}")
        except Exception as e:
            logger.error(f"Failed to decode JSON: {e}")
            return None
        db_gen = self.get_db()
        db = await anext(db_gen)
        try:
            genres = action_request.genres
            try:
                user_info = await get_user_info(db, action_request.user_id)
                for i in genres:
                    if i in user_info.genres_preference:
                        user_info.genres_preference[i] = (user_info.genres_preference[i] + action_request.rate)/2
                    else:
                        user_info.genres_preference[i] = action_request.rate
                await update_user_info(db, user_id=action_request.user_id, genres_preference=user_info.genres_preference)
            except Exception as e:
                genres_preferences = {}
                for genre in genres:
                    genres_preferences[genre] = action_request.rate
                try:
                    user = model.UserInfo(
                        user_id=action_request.user_id,
                        genres_preference=genres_preferences,
                        avg_rating=0,
                        tags_preference={},
                        svd_vector=[],
                    )
                    await create_user_info(db, user)
                except Exception as e:
                    logger.error(f"Can't create new user from kafka rate event: {action_request}. Error: {e}")
                    return        
            logger.info(f"Data saved to database: {action_request}")
        except Exception as e:
            logger.error(f"Failed to save data to database: {e}")
        pass

    async def consume(self):
        try:
            async for message in self.consumer:
                await self.processing(message)
        except Exception as e:
            logger.error(f"Got error from Kafka: {e}")
        finally:
            await self.consumer.stop()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
