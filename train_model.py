# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Ensure the directory exists
os.makedirs("data/models", exist_ok=True)

def train_and_save_model():
    # Load sample data
    df = pd.read_csv("data/sample_network_data/network_stats.csv")
    features = df[['bandwidth', 'latency', 'signal_strength']]
    target = df['uptime']

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(features, target)

    # Save model
    with open("data/models/network_predictor.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Trained and saved network_predictor.pkl")

if __name__ == "__main__":
    train_and_save_model()