from fastapi import FastAPI, Response, status, Depends
from contextlib import asynccontextmanager
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import create_user_info, get_user_info, get_all_users
from app.config import settings
from app.kafka_reader import KafkaConsumerService
import logging
import app.model as model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.LOG_FILENAME),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

kafka_service = KafkaConsumerService(topic=settings.KAFKA_TOPIC, bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS, get_db=get_db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Service started")
    # Here kafka service init
    # asyncio.create_task(kafka_service.start())
    await kafka_service.start()
    asyncio.create_task(kafka_service.consume())
    yield
    await kafka_service.stop()
    logger.info("Service stopped")

app = FastAPI(lifespan=lifespan)


@app.post("/preferences/")
async def create_user(user: model.UserInfo, response : Response, db: AsyncSession = Depends(get_db)):
    # пока что вместо кафки
    logger.info(f"create preferences for user with id = {user.user_id}")
    try:
        await create_user_info(db, user)
        return {"status" : "ok"}
    except:
        response.status_code = status.HTTP_409_CONFLICT
        return {"status" : "dublicate"}

@app.get("/preferences/{user_id}")
async def user_info(user_id : int, response : Response, db: AsyncSession = Depends(get_db)):
    try:
        user_preferences = await get_user_info(db, user_id)
        print(user_preferences)
        if user_preferences is None:
            raise Exception("User not found")
        logger.info(f"get preferences OK for user with id={user_id}")
        return user_preferences
    except Exception as e:
        logger.error(f"get preferences error: {str(e)}")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status" : "user not found"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
