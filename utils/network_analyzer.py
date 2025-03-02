# utils/network_analyzer.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
import logging
from typing import Dict, List, Tuple
import os

logger = logging.getLogger(__name__)

class NetworkAnalyzer:
    def __init__(self, model_path: str = None):
        """Initialize with an optional pre-trained model."""
        if model_path and os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            logger.info(f"Loaded pre-trained model from {model_path}")
        else:
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            logger.info("Initialized new RandomForestRegressor model")

    def load_data(self, data_path: str) -> pd.DataFrame:
        """Load network data from a CSV file."""
        try:
            df = pd.read_csv(data_path)
            required_columns = ['bandwidth', 'latency', 'signal_strength', 'uptime']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Missing required columns in data.")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare data for prediction."""
        features = df[['bandwidth', 'latency', 'signal_strength']]
        target = df['uptime']
        return features, target

    def train_model(self, features: pd.DataFrame, target: pd.Series):
        """Train the predictive model."""
        try:
            self.model.fit(features, target)
            logger.info("Network prediction model trained successfully")
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def predict_downtime(self, features: pd.DataFrame) -> List[float]:
        """Predict network uptime/downtime."""
        try:
            predictions = self.model.predict(features)
            return predictions.tolist()
        except Exception as e:
            logger.error(f"Error predicting downtime: {str(e)}")
            raise

    def analyze_energy_efficiency(self, df: pd.DataFrame) -> Dict[str, float]:
        """Estimate energy usage based on network metrics."""
        try:
            # Simplified energy model: energy = bandwidth * uptime * scaling factor
            energy_usage = df['bandwidth'] * df['uptime'] * 0.1
            return {
                "avg_energy_usage": energy_usage.mean(),
                "total_energy_usage": energy_usage.sum()
            }
        except Exception as e:
            logger.error(f"Error analyzing energy efficiency: {str(e)}")
            raise