from datetime import date as dtdate
from datetime import datetime
from typing import Dict, List, Optional, Set

from pydantic import BaseModel, Field, validator

from app.db_models import WeatherData, WeatherType

DEFAULT_LIMIT = 100


class WeatherDataParams(BaseModel):
    class Config:
        use_enum_values = True

    limit: Optional[int] = Field(default=DEFAULT_LIMIT)
    date: Optional[dtdate] = Field(default=None)
    weather: Optional[WeatherType] = Field(default=None)

    @classmethod
    def valid_filters(cls) -> Set[str]:
        return set(cls.__fields__.keys()) - {"limit"}

    @validator("date")
    def convert_date_to_datetime(cls, date_value: dtdate) -> datetime:
        if date_value is not None:
            return datetime.combine(date_value, datetime.min.time())
        return None


class WeatherDataResults(BaseModel):
    data: List[WeatherData]
    total_count: int


class BulkCreateSummary(BaseModel):
    success_count: Dict[str, int]
    error_count: int
    errors: Set[str]
