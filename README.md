# Neural-Nexus Weather API

A Python-based weather information service that fetches weather data using the OpenWeather API.

## Features
- Fetch real-time weather data for any city
- Temperature in Celsius
- Humidity information
- Weather description

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set your OpenWeather API key as environment variable:
   ```bash
   export WEATHER_API_KEY='your_api_key'
   ```

## Usage
```python
from utils.api_handler import WeatherHandler

weather = WeatherHandler(api_key='your_api_key')
result = weather.get_weather_info("weather in London")
print(result)
```
