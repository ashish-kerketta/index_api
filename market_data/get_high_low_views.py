# market_data/views.py
import yfinance as yf
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_high_low(request, ticker):
    try:
        # Fetch stock data for the given ticker symbol for the last 1 month (1-day candles)
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo", interval="1d")  # 1-month daily candlestick data

        if not data.empty:
            # Calculate high and low for each required period based on daily data
            # Get the most recent day's data
            current_day = data.iloc[-1]
            current_day_high_low = {
                "high": f"{current_day['High']:.2f}",  # Format to 2 decimal places
                "low": f"{current_day['Low']:.2f}"     # Format to 2 decimal places
            }

            # Get the previous day's data if available
            previous_day = data.iloc[-2] if len(data) > 1 else current_day
            previous_day_high_low = {
                "high": f"{previous_day['High']:.2f}",  # Format to 2 decimal places
                "low": f"{previous_day['Low']:.2f}"     # Format to 2 decimal places
            }

            # Get high and low for the last week (last 7 trading days)
            weekly_data = data[-7:]  # Get last 7 entries
            weekly_high = weekly_data['High'].max()
            weekly_low = weekly_data['Low'].min()
            weekly_high_low = {
                "high": f"{weekly_high:.2f}",  # Format to 2 decimal places
                "low": f"{weekly_low:.2f}"      # Format to 2 decimal places
            }

            # Get high and low for the last month (all entries in the dataset)
            monthly_high = data['High'].max()
            monthly_low = data['Low'].min()
            monthly_high_low = {
                "high": f"{monthly_high:.2f}",  # Format to 2 decimal places
                "low": f"{monthly_low:.2f}"      # Format to 2 decimal places
            }

            # Return response with calculated high/low values
            return Response({
                "ticker": ticker,
                "currentDayHighLow": current_day_high_low,
                "previousDayHighLow": previous_day_high_low,
                "weeklyHighLow": weekly_high_low,
                "monthlyHighLow": monthly_high_low
            })
        else:
            return Response({"error": "No data available for the ticker."}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

