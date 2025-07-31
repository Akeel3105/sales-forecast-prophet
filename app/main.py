from fastapi import FastAPI, Query
from typing import Optional
from app.model import forecast_sales

app = FastAPI(
    title="🧠 Wellness Sales Forecasting API",
    description="Forecast daily sales using Prophet model.",
    version="1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to the Sales Forecasting API"}

@app.get("/forecast")
def get_forecast(
    level: str = Query("overall", enum=["overall", "store", "product"]),
    store_id: Optional[str] = None,
    product_id: Optional[str] = None,
    days: int = 30
):
    forecast = forecast_sales(
        level=level,
        store_id=store_id,
        product_id=product_id,
        days=days
    )
    return forecast
