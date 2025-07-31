from app.model import forecast_sales

def test_forecast_output_keys():
    result = forecast_sales(level="overall", days=5)
    assert isinstance(result, list)
    assert "ds" in result[0]
    assert "yhat" in result[0]
    assert "yhat_lower" in result[0]
    assert "yhat_upper" in result[0]

def test_forecast_length():
    result = forecast_sales(level="overall", days=10)
    assert len(result) == 10
