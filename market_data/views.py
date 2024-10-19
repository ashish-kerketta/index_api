# market_data/views.py
import yfinance as yf
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_nse_index(request, ticker):
    try:
        # Fetch stock data for the given ticker symbol for the last 1 month (1-day candles)
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo", interval="1d")  # 1-month daily candlestick data

        if not data.empty:
            # Create a list of candlestick data
            candle_data = []
            for index, row in data.iterrows():
                candle_data.append({
                    "date": index.strftime('%Y-%m-%d'),  # Format date
                    "open": row['Open'],
                    "high": row['High'],
                    "low": row['Low'],
                    "close": row['Close'],
                    "volume": row['Volume'],
                })
            
            # Extract high/low for current day (first entry)
            current_day = candle_data[0]
            current_day_high_low = {
                "high": current_day['high'],
                "low": current_day['low']
            }
            
            # Extract high/low for previous day (second entry)
            previous_day = candle_data[1] if len(candle_data) > 1 else current_day
            previous_day_high_low = {
                "high": previous_day['high'],
                "low": previous_day['low']
            }
            
            # Extract high/low for the last week (up to 8 days)
            weekly_candles = candle_data[:8]  # Last 8 days (including today)
            weekly_high = max([candle['high'] for candle in weekly_candles])
            weekly_low = min([candle['low'] for candle in weekly_candles])
            weekly_high_low = {
                "high": weekly_high,
                "low": weekly_low
            }
            
            # Extract high/low for the entire month (all candles in the dataset)
            monthly_high = max([candle['high'] for candle in candle_data])
            monthly_low = min([candle['low'] for candle in candle_data])
            monthly_high_low = {
                "high": monthly_high,
                "low": monthly_low
            }

            # Return response with all calculated high/low values
            return Response({
                "ticker": ticker,
                "candles": candle_data,
                "currentDayHighLow": current_day_high_low,
                "previousDayHighLow": previous_day_high_low,
                "weeklyHighLow": weekly_high_low,
                "monthlyHighLow": monthly_high_low
            })
        else:
            return Response({"error": "No data available for the ticker."}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
