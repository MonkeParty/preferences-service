from fastapi import FastAPI, Response, status
from contextlib import asynccontextmanager
import asyncio
import config
from kafka_reader import KafkaConsumerService
import logging
import model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILENAME),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

kafka_service = KafkaConsumerService(topic=config.KAFKA_TOPIC, bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Service started")
    # Here kafka service init
    # asyncio.create_task(kafka_service.start())
    # asyncio.create_task(kafka_service.consume())
    yield
    # await kafka_service.stop()
    logger.info("Service stopped")

app = FastAPI(lifespan=lifespan)

@app.post("/action")
async def root(requestBody : model.ActionRequest, response: Response):
    # MOCK
    logger.info(f"Got action request: {str(requestBody)}")
    # Here we update data for user in database
    return {"film_id" : requestBody.film_id, "value" : requestBody.value}

@app.get("/preferences/{user_id}")
async def user_info(user_id : int, response : Response):
    # MOCK
    # try select from database user_id
    # ....

    # if user is not exist - return 404
    if user_id != 1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    # return data from database
    return {"user_id" : user_id, "avg_rating" : 4.5, "w" : [1,2,3,4,]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
