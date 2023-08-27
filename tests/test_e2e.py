import os
import requests

POST_WEATHER_DATA_URL = "http://weather-service:8000/weather-data/csv"
GET_WEATHER_DATA_URL = "http://weather-service:8000/weather-data"


def test_valid_csv_file(valid_csv_file):
    file_path, summary = valid_csv_file
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 200
        assert (
            response.json().get("success_count").get("weather_data")
            == summary["success_count"]
        )
        assert response.json().get("error_count") == summary["error_count"]
        assert response.json().get("errors") == summary["errors"]


def test_missing_header_csv_file(missing_header_csv_file):
    file_path, error_msg = missing_header_csv_file
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 400
        assert response.json().get("detail") == error_msg


def test_empty_csv_file(empty_file):
    file_path = empty_file
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 400
        assert (
            response.json().get("detail")
            == "Invalid CSV file. Please check the headers."
        )


def test_non_csv_file(non_csv_file):
    file_path = non_csv_file
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 400
        assert (
            response.json().get("detail")
            == "Invalid file format. Only CSV files are allowed."
        )


def test_extra_headers_csv_file(extra_headers_csv):
    file_path = extra_headers_csv
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 400
        assert (
            response.json().get("detail")
            == "Invalid CSV file. Please check the headers."
        )


def test_invalid_weather_csv(invalid_weather_csv):
    file_path, summary = invalid_weather_csv
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 200
        assert (
            response.json().get("success_count").get("weather_data")
            == summary["success_count"]
        )
        assert response.json().get("error_count") == summary["error_count"]
        assert response.json().get("errors") == summary["errors"]


def test_large_csv(data_dir):
    file_path = os.path.join(data_dir, "seattle-weather-10k.csv")
    with open(file_path, "rb") as file:
        response = requests.post(
            POST_WEATHER_DATA_URL,
            files={"file": file},
        )

        assert response.status_code == 200
        assert response.json().get("success_count").get("weather_data") == 10000
        assert response.json().get("error_count") == 0
        assert response.json().get("errors") == []


def test_get_weather_data_with_default_limit():
    response = requests.get(GET_WEATHER_DATA_URL)
    assert response.status_code == 200
    assert response.json().get("total_count") == 100
    assert len(response.json().get("data")) == 100


def test_get_weather_data_with_limit():
    response = requests.get(GET_WEATHER_DATA_URL, params={"limit": 5})
    assert response.status_code == 200
    assert response.json().get("total_count") == 5
    assert len(response.json().get("data")) == 5


def test_get_weather_data_with_weather():
    response = requests.get(GET_WEATHER_DATA_URL, params={"weather": "rain"})
    assert response.status_code == 200
    assert all([data["weather"] == "rain" for data in response.json().get("data")])


def test_get_weather_data_with_nonexisting_weather():
    response = requests.get(GET_WEATHER_DATA_URL, params={"weather": "tornado"})
    assert response.status_code == 400
    assert (
        response.json().get("detail")[0]
        == "Invalid value for query -> weather. Allowed values are: ['sun', 'rain', 'snow', 'cloudy', 'fog', 'drizzle']"
    )


def test_get_weather_data_with_existing_date():
    response = requests.get(GET_WEATHER_DATA_URL, params={"date": "2012-03-09"})
    assert response.status_code == 200
    assert all(
        [data["date"] == "2012-03-09T00:00:00" for data in response.json().get("data")]
    )


def test_get_weather_data_with_nonexisting_date():
    response = requests.get(GET_WEATHER_DATA_URL, params={"date": "2023-08-27"})
    assert response.status_code == 200
    assert response.json().get("total_count") == 0
    assert len(response.json().get("data")) == 0


def test_get_weather_data_all_filter_params():
    response = requests.get(
        GET_WEATHER_DATA_URL,
        params={"weather": "rain", "date": "2012-03-09", "limit": 5},
    )
    assert response.status_code == 200
    assert response.json().get("total_count") == 5
    assert len(response.json().get("data")) == 5
    assert all(
        [
            data["date"] == "2012-03-09T00:00:00" and data["weather"] == "rain"
            for data in response.json().get("data")
        ]
    )
