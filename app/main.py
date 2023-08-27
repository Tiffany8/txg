import logging
import os
import sys

import motor
from fastapi import FastAPI, HTTPException, status
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
    ServerSelectionTimeoutError,
)

from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = FastAPI()

app.include_router(router)

app.exception_handler(RequestValidationError)(validation_exception_handler)


@app.on_event("startup")
def startup_db_client():
    try:
        app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(
            os.getenv("MONGO_URL")
        )
        app.database = app.mongodb_client.app_database
        print("Connected to the MongoDB database!")
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
        # fyi - raise with no argument preserves original traceback
        logging.error("An unexpected error occurred:", str(e))
        raise


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
