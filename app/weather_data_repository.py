from typing import List

from app.api_schemas import WeatherDataParams
from app.db_models import WeatherData


class WeatherDataRepository:
    """
    A class that represents a repository for weather data.

    Args:
        client: The client object used to interact with the weather data collection.

    Attributes:
        client: The client object used to interact with the weather data collection.

    """

    def __init__(self, client):
        self.client = client

    async def find_weather_data(self, params: WeatherDataParams):
        """
        Finds weather data based on the provided parameters.

        Args:
            params: An instance of WeatherDataParams containing the filter parameters.

        Returns:
            A list of weather data objects that match the filter parameters.

        """

        def build_filter(params: WeatherDataParams):
            return {
                key: value
                for key, value in params.dict().items()
                if key in WeatherDataParams.valid_filters() and value is not None
            }

        filter_query = build_filter(params)

        return await self.client.weather_data.find(filter_query).to_list(
            length=params.limit
        )

    async def insert_weather_data(self, weather_data: List[WeatherData]) -> List[str]:
        """
        Inserts weather data into the repository.

        Args:
            weather_data: A list of WeatherData objects to be inserted.

        Returns:
            List of the inserted weather data ids.
        """
        return (await self.client.weather_data.insert_many(weather_data)).inserted_ids
