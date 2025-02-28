import google.generativeai as genai
import requests
import logging
from typing import Dict, Any, Union, List
from PIL import Image
import mimetypes
import os
from config import GEMINI_MODEL

logger = logging.getLogger(__name__)

class GeminiHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
    def _process_file_input(self, file_path: str) -> Union[str, Image.Image, List]:
        mime_type, _ = mimetypes.guess_type(file_path)
        
        if mime_type:
            if mime_type.startswith('image/'):
                return Image.open(file_path)
            elif mime_type.startswith(('text/', 'application/')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        return None

    async def generate_response(self, prompt: str, file_path: str = None, context: list = None) -> str:
        try:
            if not context:
                context = []
            
            if file_path:
                content = self._process_file_input(file_path)
                if isinstance(content, Image.Image):
                    response = self.model.generate_content([prompt, content])
                else:
                    response = self.model.generate_content([prompt, str(content)])
            else:
                response = self.model.generate_content(prompt, generation_config=None)
            
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return f"I encountered an error processing your request: {str(e)}"

class WeatherHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather_info(self, query: str) -> str:
        try:
            city = self._extract_city(query)
            
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return self._format_weather_response(data)
        except Exception as e:
            logger.error(f"Weather API error: {str(e)}")
            raise
            
    def _extract_city(self, query: str) -> str:
        words = query.lower().split()
        try:
            idx = words.index("in")
            return " ".join(words[idx + 1:])
        except ValueError:
            return " ".join(words[-1:])
            
    def _format_weather_response(self, data: Dict[str, Any]) -> str:
        return (f"Weather in {data['name']}: {data['weather'][0]['description']}. "
                f"Temperature: {data['main']['temp']}°C, "
                f"Humidity: {data['main']['humidity']}%")
