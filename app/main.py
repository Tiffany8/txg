import logging
import os
import sys

import motor
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
    ServerSelectionTimeoutError,
)

from app.exception_handlers import validation_exception_handler
from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI()

app.include_router(router)

app.exception_handler(RequestValidationError)(validation_exception_handler)


from dataclasses import dataclass


@dataclass
class MongodDbConfigs:
    client: str
    dbname: str


def get_mongodb_configs():
    if os.getenv("APP_ENV") == "test":
        return MongodDbConfigs(
            client=motor.motor_asyncio.AsyncIOMotorClient(os.getenv("TEST_MONGO_URL")),
            dbname=os.getenv("TEST_MONGODB_NAME"),
        )
    else:
        return MongodDbConfigs(
            client=motor.motor_asyncio.AsyncIOMotorClient(
                os.getenv("MONGO_URL", "mongodb://localhost:27017")
            ),
            dbname=os.getenv("MONGODB_NAME", "localdb"),
        )


@app.on_event("startup")
def startup_db_client():
    try:
        configs = get_mongodb_configs()
        mongo_client = configs.client
        db_name = configs.dbname
        app.database = mongo_client[db_name]
        print(f"Connected to the MongoDB database: {db_name}")
    except (
        ConfigurationError,
        ServerSelectionTimeoutError,
        ConnectionFailure,
    ) as error:
        logging.error("Configuration Error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error. Please try again later.",
        )
    except Exception as e:
        logging.error("An unexpected error occurred:", str(e))
        raise


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
