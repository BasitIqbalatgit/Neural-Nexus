# app/components/visualizations.py
import streamlit as st
import pandas as pd
from utils.network_analyzer import NetworkAnalyzer
from utils.geo_processor import GeoProcessor
import os
import plotly.express as px  # For simple visualizations
import logging

logger = logging.getLogger(__name__)


def display_network_analysis(network_analyzer: NetworkAnalyzer):
    st.subheader("Network Analysis")
    st.write(
        "Upload a CSV file with network data (columns: bandwidth, latency, signal_strength, uptime) to predict network uptime and analyze energy efficiency.")

    uploaded_data = st.file_uploader("Upload network data (CSV)", type=["csv"], key="network_data")
    if uploaded_data:
        temp_file = "temp_network_data.csv"
        with open(temp_file, "wb") as f:
            f.write(uploaded_data.read())

        # Load and process data
        try:
            df = network_analyzer.load_data(temp_file)
            features, target = network_analyzer.preprocess_data(df)
            network_analyzer.train_model(features, target)
            predictions = network_analyzer.predict_downtime(features)
            energy_stats = network_analyzer.analyze_energy_efficiency(df)

            # Debugging: Log predictions length
            logger.debug(f"Number of predictions: {len(predictions)}")
            st.write(f"Debug: Total predictions generated: {len(predictions)}")

            # Display Predictions in a Table
            st.markdown("### Predicted Network Uptime")
            st.write("The table below shows predicted uptime percentages for the first 5 data points.")
            pred_df = pd.DataFrame({
                "Data Point": [f"Point {i + 1}" for i in range(min(5, len(predictions)))],
                "Predicted Uptime (%)": [f"{p * 100:.2f}%" for p in predictions[:5]]
            })
            st.table(pred_df)

            # Display Energy Efficiency Stats
            st.markdown("### Energy Efficiency Analysis")
            st.write("Estimated energy usage based on bandwidth and uptime data:")
            energy_df = pd.DataFrame({
                "Metric": ["Average Energy Usage (units)", "Total Energy Usage (units)"],
                "Value": [f"{energy_stats['avg_energy_usage']:.2f}", f"{energy_stats['total_energy_usage']:.2f}"]
            })
            st.table(energy_df)

            # Plot Uptime Prediction Trend
            st.markdown("### Uptime Prediction Trend")
            if predictions and len(predictions) > 0:
                # Use all predictions if less than 10, otherwise first 10
                num_points = min(10, len(predictions))
                x_values = [f"Point {i + 1}" for i in range(num_points)]
                y_values = predictions[:num_points]

                fig = px.line(x=x_values, y=y_values,
                              labels={"x": "Data Point", "y": "Predicted Uptime (fraction)"},
                              title=f"Uptime Predictions (First {num_points} Points)")
                fig.update_traces(mode="lines+markers")  # Add markers for clarity
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No predictions available to plot.")

        except Exception as e:
            logger.error(f"Error in network analysis: {str(e)}")
            st.error(f"Error processing network data: {str(e)}")

        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def display_node_placement(geo_processor: GeoProcessor):
    st.subheader("Node Placement Optimization")
    st.write("Upload a GeoJSON file with location data (e.g., schools) to suggest optimal network node placements.")

    geo_file = st.file_uploader("Upload geo data (GeoJSON)", type=["geojson"], key="geo_data")
    if geo_file:
        temp_file = "temp_geo_data.json"
        with open(temp_file, "wb") as f:
            f.write(geo_file.read())

        gdf = geo_processor.load_geo_data(temp_file)
        nodes = geo_processor.suggest_node_placement(gdf)
        map_obj = geo_processor.visualize_map(nodes)

        # Display Suggested Node Locations in a Table
        st.markdown("### Suggested Node Locations")
        st.write("The table below shows the first 5 suggested network node locations (latitude, longitude).")
        nodes_df = pd.DataFrame({
            "Node ID": [f"Node {i + 1}" for i in range(min(5, len(nodes)))],
            "Latitude": [f"{lat:.6f}" for lat, _ in nodes[:5]],
            "Longitude": [f"{lon:.6f}" for _, lon in nodes[:5]]
        })
        st.table(nodes_df)

        # Display Map
        st.markdown("### Node Placement Map")
        st.write("Interactive map showing all suggested node locations.")
        st.components.v1.html(map_obj._repr_html_(), height=500)

        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)