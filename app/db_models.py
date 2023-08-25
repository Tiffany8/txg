from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator


class WeatherType(Enum):
    SUN = "sun"
    RAIN = "rain"
    SNOW = "snow"
    CLOUDY = "cloudy"
    FOG = "fog"
    DRIZZLE = "drizzle"


class WeatherData(BaseModel):
    class Config:
        use_enum_values = True

    id: Optional[str]
    date: datetime
    precipitation: float
    temp_max: float
    temp_min: float
    wind: float
    weather: WeatherType
    created_at: datetime = datetime.now()

    @validator("date", pre=True)
    def convert_date_to_datetime(cls, date_value: str | date) -> datetime:
        """
        Converts the date value to a datetime object.

        Args:
            date_value: The date value to convert.

        Returns:
            Datetime object.

        """
        if isinstance(date_value, str):
            try:
                date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    f"Invalid date format for {date_value}. Expected 'YYYY-MM-DD'"
                )

        if isinstance(date_value, date) and not isinstance(date_value, datetime):
            return datetime.combine(date_value, datetime.min.time())

        return date_value
