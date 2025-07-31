from app.model import forecast_sales

# Example: Forecast 15 days of total sales across all stores/products
output = forecast_sales(level="overall", days=15)

# Print first 5 predictions
for row in output[:5]:
    print(row)
