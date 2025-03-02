# generate_sample_data.py
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import os

# Ensure the directory exists
os.makedirs("data/sample_network_data", exist_ok=True)


# 1. Generate Network Stats CSVs
def generate_network_stats(filename: str, num_rows: int, bandwidth_range: tuple, latency_range: tuple,
                           signal_range: tuple, uptime_range: tuple):
    """Generate a CSV with network performance data."""
    np.random.seed(42)  # For reproducibility
    data = {
        "node_id": [f"Node_{i + 1}" for i in range(num_rows)],
        "bandwidth": np.random.uniform(bandwidth_range[0], bandwidth_range[1], num_rows),  # Mbps
        "latency": np.random.uniform(latency_range[0], latency_range[1], num_rows),  # ms
        "signal_strength": np.random.uniform(signal_range[0], signal_range[1], num_rows),  # dBm
        "uptime": np.random.uniform(uptime_range[0], uptime_range[1], num_rows)  # Percentage
    }
    df = pd.DataFrame(data)
    df.to_csv(f"data/sample_network_data/{filename}", index=False)
    print(f"Generated {filename}")


# 2. Generate Geospatial GeoJSONs
def generate_geo_data(filename: str, num_locations: int, lat_range: tuple, lon_range: tuple,
                      population_range: tuple):
    """Generate a GeoJSON with school locations."""
    np.random.seed(42)
    lats = np.random.uniform(lat_range[0], lat_range[1], num_locations)
    lons = np.random.uniform(lon_range[0], lon_range[1], num_locations)
    points = [Point(lon, lat) for lon, lat in zip(lons, lats)]

    gdf = gpd.GeoDataFrame(
        {"name": [f"School_{i + 1}" for i in range(num_locations)],
         "population": np.random.randint(population_range[0], population_range[1], num_locations)},
        geometry=points,
        crs="EPSG:4326"
    )
    gdf.to_file(f"data/sample_network_data/{filename}", driver="GeoJSON")
    print(f"Generated {filename}")


if __name__ == "__main__":
    # Network Stats Scenarios
    # Rural: Low bandwidth, high latency, weaker signal
    generate_network_stats(
        "network_stats_rural.csv",
        num_rows=50,
        bandwidth_range=(1, 20),
        latency_range=(100, 300),
        signal_range=(20, 60),
        uptime_range=(0.7, 0.9)
    )

    # Urban: High bandwidth, low latency, strong signal
    generate_network_stats(
        "network_stats_urban.csv",
        num_rows=50,
        bandwidth_range=(50, 100),
        latency_range=(10, 50),
        signal_range=(80, 100),
        uptime_range=(0.9, 1.0)
    )

    # Mixed: Varied conditions
    generate_network_stats(
        "network_stats_mixed.csv",
        num_rows=100,
        bandwidth_range=(5, 80),
        latency_range=(20, 200),
        signal_range=(30, 90),
        uptime_range=(0.75, 0.98)
    )

    # Geospatial Scenarios
    # Rural: Sparse locations (e.g., rural Africa)
    generate_geo_data(
        "school_locations_rural.geojson",
        num_locations=10,
        lat_range=(-5, 5),  # Near equator
        lon_range=(20, 30),  # Eastern Africa
        population_range=(50, 200)
    )

    # Urban: Dense locations (e.g., city-like cluster)
    generate_geo_data(
        "school_locations_urban.geojson",
        num_locations=30,
        lat_range=(40, 41),  # Near a city (e.g., New York latitude)
        lon_range=(-74, -73),  # New York longitude
        population_range=(200, 1000)
    )