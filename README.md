# Weather Data Service ☀️🌥️🌧️❄️🌁
API interface for storing and accessing historical weather data

## Routes:
`GET /weather-data`: Retrieve weather data based on various optional parameters like date, weather type, and data limit.

`POST /weather-data/csv`: Upload a CSV file to add bulk weather data. Only CSV files with valid headers are accepted.

## How to run the service and execute the tests
1. Download the project
```bash
git clone https://github.com/Tiffany8/txg.git
```

2. Make the script executable
```bash
chmod +x run_service_and_e2e.sh
```

3. Run the script:
    ```bash
    ./run_service_and_e2e.sh
    ```
    
    To include end-to-end tests, use the `--e2e` flag:
    ```bash
    ./run_service_and_e2e.sh --e2e
    ```


## OpenAI Interface
Once the service is running, you can also navigate to localhost:8000/docs in your web browser to explore the API and understand the parameters via the OpenAPI interface.

## Example commands to interact with the Weather Service
I like to use [httpie](https://httpie.io)

to populate your database:
    `http -f POST localhost:8000/weather-data/csv file@/PATH/to/data/seattle-weather-10k.csv`

to get:

data from March 9, 2012:
`http localhost:8000/weather-data date==2012-03-09`

rain data:
`http localhost:8000/weather-data weather==rain`