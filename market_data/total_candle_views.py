# market_data/total_candle_views.py
import yfinance as yf
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_nse_5min_candles(request, ticker):
    try:
        # Fetch stock data for the given ticker symbol at 5-minute intervals
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="5m")  # Get 5-minute candles for today
        
        if not data.empty:
            # Limit to the most recent 60 candles to ensure we can calculate SMA50
            data = data.tail(60)
            
            # Check how many candles are fetched
            total_candles = len(data)
            
            # Prepare the response with the number of candles fetched
            response_data = {
                "ticker": ticker,
                "total_candles_fetched": total_candles,
                "candles": data.to_dict('records'),  # Optional: include raw candle data for debugging
            }

            return Response(response_data)
        else:
            return Response({"error": "No data available for the ticker."}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
