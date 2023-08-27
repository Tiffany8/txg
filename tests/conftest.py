import os
import pytest


@pytest.fixture
def data_dir():
    return "/tests/mock-data"


@pytest.fixture
def valid_csv_file(data_dir):
    # Create the valid file in the data directory
    csv_data = "date,precipitation,temp_max,temp_min,wind,weather\n2012-06-29,0.3,21.7,15.0,1.9,rain\n2012-07-04,0.0,20.6,9.4,3.8,sun"
    with open(os.path.join(data_dir, "valid.csv"), "w") as file:
        file.write(csv_data)

    summary = {"success_count": 2, "error_count": 0, "errors": []}
    yield os.path.join(data_dir, "valid.csv"), summary

    # Clean up the created file after the test
    os.remove(os.path.join(data_dir, "valid.csv"))


@pytest.fixture
def missing_header_csv_file(data_dir):
    # Create the invalid file in the data directory
    csv_data = "date,precipitation,temp_max,temp_min,wind\n2022-01-01,0.5,25.0,15.0,10.0\n2022-01-02,0.0,28.0,18.0,12.0"
    with open(os.path.join(data_dir, "missing_header.csv"), "w") as file:
        file.write(csv_data)

    response_message = "Invalid CSV file. Please check the headers."

    yield os.path.join(data_dir, "missing_header.csv"), response_message

    # Clean up the created file after the test
    os.remove(os.path.join(data_dir, "missing_header.csv"))


@pytest.fixture
def empty_file(data_dir):
    # Create the invalid file in the data directory
    csv_data = ""
    with open(os.path.join(data_dir, "empty.csv"), "w") as file:
        file.write(csv_data)

    yield os.path.join(data_dir, "empty.csv")

    # Clean up the created file after the test
    os.remove(os.path.join(data_dir, "empty.csv"))


@pytest.fixture
def non_csv_file(data_dir):
    # Create the invalid file in the data directory
    csv_data = "This is not a CSV file"
    with open(os.path.join(data_dir, "non_csv.txt"), "w") as file:
        file.write(csv_data)

    yield os.path.join(data_dir, "non_csv.txt")

    # Clean up the created file after the test
    os.remove(os.path.join(data_dir, "non_csv.txt"))


@pytest.fixture
def extra_headers_csv(data_dir):
    # Create the invalid file in the data directory
    csv_data = "date,precipitation,temp_max,temp_min,wind,weather,humidity\n2022-01-01,0.5,25.0,15.0,10.0,sun,55\n2022-01-02,0.0,28.0,18.0,12.0,cloudy,55\n2022-01-03,0.0,28.0,18.0,12.0,cloudy,55"
    with open(os.path.join(data_dir, "extra_headers.csv"), "w") as file:
        file.write(csv_data)

    yield os.path.join(data_dir, "extra_headers.csv")

    # Clean up the created file after the test
    os.remove(os.path.join(data_dir, "extra_headers.csv"))


@pytest.fixture
def invalid_weather_csv(data_dir):
    # Create the invalid file in the data directory
    csv_data = "date,precipitation,temp_max,temp_min,wind,weather\n2012-06-29,0.3,21.7,15.0,1.9,cloudy\n2012-07-04,0.0,20.6,9.4,3.8,ChanceOfMeatballs"
    with open(os.path.join(data_dir, "invalid_weather.csv"), "w") as file:
        file.write(csv_data)

    summary = {
        "success_count": 1,
        "error_count": 1,
        "errors": ["Invalid weather: ChanceOfMeatballs"],
    }
    yield os.path.join(data_dir, "invalid_weather.csv"), summary

    # Clean up the created file after the test
    os.remove(os.path.join(data_dir, "invalid_weather.csv"))
