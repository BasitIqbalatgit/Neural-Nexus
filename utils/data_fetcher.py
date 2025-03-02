# utils/data_fetcher.py
import requests
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = None  # Placeholder for real API (e.g., Giga API)

    def fetch_network_data(self, source: str = "sample") -> pd.DataFrame:
        """Fetch network data from an API or generate sample data."""
        if source == "api" and self.base_url:
            return self._fetch_from_api()
        else:
            return self._generate_sample_data()

    def _fetch_from_api(self) -> pd.DataFrame:
        """Fetch data from a real-time API (placeholder)."""
        try:
            if not self.api_key or not self.base_url:
                raise ValueError("API key or URL not configured.")
            response = requests.get(self.base_url, params={"key": self.api_key})
            response.raise_for_status()
            data = response.json()
            # Convert to DataFrame (customize based on actual API response)
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error fetching API data: {str(e)}")
            raise

    def _generate_sample_data(self) -> pd.DataFrame:
        """Generate sample network data for testing."""
        try:
            np.random.seed(42)
            data = {
                "bandwidth": np.random.uniform(1, 100, 100),  # Mbps
                "latency": np.random.uniform(10, 200, 100),   # ms
                "signal_strength": np.random.uniform(20, 100, 100),  # dBm
                "uptime": np.random.uniform(0.8, 1.0, 100)    # Percentage
            }
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error generating sample data: {str(e)}")
            raise