from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from app.api_schemas import BulkCreateSummary, WeatherDataParams, WeatherDataResults
from app.db_models import WeatherData
from app.route_helpers import validate_csv_headers
from app.services import get_weather_data, process_and_save_weather_data_csv

router = APIRouter()


@router.get("/weather-data", response_model=WeatherDataResults)
async def read_weather_data(
    request: Request, params: WeatherDataParams = Depends(WeatherDataParams)
):
    return await get_weather_data(request.app.database, params)


@router.post("/weather-data/csv", response_model=BulkCreateSummary)
async def upload_weather_data_csv(request: Request, file: UploadFile = File(...)):
    """
    Uploads a CSV file containing weather data.

    """
    if file is None:
        raise HTTPException(status_code=400, detail="No file provided")
    if file.content_type != "text/csv":
        raise HTTPException(
            status_code=400, detail="Invalid file format. Only CSV files are allowed."
        )

    is_valid = validate_csv_headers(file, list(WeatherData.__fields__.keys()))
    if not is_valid:
        raise HTTPException(
            status_code=400, detail="Invalid CSV file. Please check the headers."
        )

    return await process_and_save_weather_data_csv(request.app.database, file)
