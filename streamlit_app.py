import streamlit as st
import pandas as pd
import plotly.express as px
from app.model import forecast_sales
from pathlib import Path

# Set page config
st.set_page_config(page_title="Wellness Sales Forecasting", layout="wide")

# Title
st.title("🧠 Wellness Sales Forecasting App")

# Load data to get dropdown options
DATA_PATH = Path(__file__).resolve().parent / "data" / "wellness_sales_data.csv"
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

# Sidebar inputs
st.sidebar.header("Forecast Settings")
level = st.sidebar.selectbox("Forecast Level", ["overall", "store", "product"])

store_id = None
product_id = None

if level == "store":
    store_id = st.sidebar.selectbox("Select Store ID", sorted(df["store_id"].dropna().unique()))
elif level == "product":
    product_id = st.sidebar.selectbox("Select Product ID", sorted(df["product_id"].dropna().unique()))

days = st.sidebar.slider("Forecast Days", min_value=7, max_value=90, value=30, step=7)

# Submit button
if st.sidebar.button("🔮 Generate Forecast"):
    st.subheader(f"Forecast for {level.upper()} - Next {days} Days")

    # Get forecast
    forecast = forecast_sales(level=level, store_id=store_id, product_id=product_id, days=days)

    if isinstance(forecast, dict) and "error" in forecast:
        st.error(forecast["error"])
    else:
        df_forecast = pd.DataFrame(forecast)
        
        # Plot
        fig = px.line(df_forecast, x="ds", y="yhat", title="Forecasted Net Sales")
        fig.add_scatter(x=df_forecast["ds"], y=df_forecast["yhat_upper"], mode='lines', name='Upper Bound', line=dict(dash='dot'))
        fig.add_scatter(x=df_forecast["ds"], y=df_forecast["yhat_lower"], mode='lines', name='Lower Bound', line=dict(dash='dot'))
        st.plotly_chart(fig, use_container_width=True)

        # Show data table
        st.dataframe(df_forecast)

        # CSV Download
        csv = df_forecast.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Forecast as CSV", csv, file_name="forecast_output.csv", mime="text/csv")
