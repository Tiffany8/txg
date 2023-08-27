import logging
from collections import defaultdict

from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from pymongo.errors import PyMongoError

from app.api_schemas import BulkCreateSummary, WeatherDataParams, WeatherDataResults
from app.db_models import WeatherData
from app.service_helpers import read_csv_in_chunks
from app.weather_data_repository import WeatherDataRepository

logger = logging.getLogger(__name__)


async def process_and_save_weather_data_csv(
    client: AsyncIOMotorClient, file: UploadFile
):
    """
    Process and save weather data from csv file
    """
    errors = set()
    error_count = 0
    success_count = defaultdict(int)

    for rows in read_csv_in_chunks(file):
        items = []

        for row in rows:
            try:
                item = WeatherData(**row)
                items.append(item.dict())
            except ValidationError as e:
                error_count += 1
                field = e.errors()[0]["loc"][0]
                errors.add(f"Invalid {field}: {row.get(field)}")
                logging.error(f"Data validation error: {str(e)}")

        if items:
            try:
                insert_result = await WeatherDataRepository(client).insert_weather_data(
                    items
                )
                success_count["weather_data"] += len(insert_result)
            except PyMongoError as e:
                error_msg = f"Database error: {str(e)}"
                errors.add(error_msg)
                error_count += 1
                logging.error(error_msg)

    return BulkCreateSummary(
        errors=errors, success_count=success_count, error_count=error_count
    )


async def get_weather_data(client: AsyncIOMotorClient, params: WeatherDataParams):
    """
    Get weather data
    """
    data = await WeatherDataRepository(client).find_weather_data(params)
    return WeatherDataResults(data=data, total_count=len(data))
