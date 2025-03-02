import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WeatherHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_info(self, query: str) -> str:
        """Fetch weather info for a location."""
        try:
            city = self._extract_city(query)
            params = {"q": city, "appid": self.api_key, "units": "metric"}
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return self._format_weather_response(data)
        except requests.RequestException as e:
            logger.error(f"Weather API error: {str(e)}")
            return f"Error fetching weather: {str(e)}"

    def _extract_city(self, query: str) -> str:
        """Extract city name from query."""
        words = query.lower().split()
        try:
            idx = words.index("in")
            return " ".join(words[idx + 1:])
        except ValueError:
            return " ".join(words[-1:])

    def _format_weather_response(self, data: Dict[str, Any]) -> str:
        """Format weather data into a readable string."""
        return (f"Weather in {data['name']}: {data['weather'][0]['description']}. "
                f"Temperature: {data['main']['temp']}°C, Humidity: {data['main']['humidity']}%")