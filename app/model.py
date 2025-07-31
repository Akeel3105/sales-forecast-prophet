import pandas as pd
from prophet import Prophet
from pathlib import Path

# Use relative path to load data (compatible with local/dev/prod)
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "wellness_sales_data.csv"
df = pd.read_csv(DATA_PATH, parse_dates=["date"])

def prepare_data(level="overall", store_id=None, product_id=None):
    data = df.copy()

    # Optional filters
    if level == "store" and store_id:
        data = data[data["store_id"] == store_id]
    elif level == "product" and product_id:
        data = data[data["product_id"] == product_id]

    # Group by date
    grouped = data.groupby("date")["net_sales"].sum().reset_index()
    grouped.rename(columns={"date": "ds", "net_sales": "y"}, inplace=True)

    return grouped

def forecast_sales(level="overall", store_id=None, product_id=None, days=30):
    ts_df = prepare_data(level=level, store_id=store_id, product_id=product_id)

    if ts_df.shape[0] < 60:
        return {"error": "Not enough data to train model."}

    model = Prophet()
    model.fit(ts_df)

    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(days)
    result["ds"] = result["ds"].dt.strftime("%Y-%m-%d")

    return result.to_dict(orient="records")
