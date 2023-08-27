#!/bin/bash

# Check if .env file exists, if not, copy .env-example to .env
if [ ! -f .env ]; then
    cp .env-example .env
    echo "Copied .env-example to .env"
fi

docker-compose up --detach db

start_service_app () {
    echo "Starting Weather Service..."
    docker-compose up --build --detach weather-service
}

# Check for --e2e flag
if [[ $1 == "--e2e" ]]; then
    echo "Running in E2E test mode..."
    
    # Start Weather Service in test mode (use the test database)
    docker-compose run --build --detach --env APP_ENV=test weather-service
    
    # Run tests
    docker-compose run --build tests
    
    # Stop the Weather Service in test mode
    docker-compose stop weather-service
fi

start_service_app

