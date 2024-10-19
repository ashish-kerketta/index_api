# market_data/nse_5min_views.py
import yfinance as yf
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_nse_5min_data(request, ticker):
    try:
        # Fetch stock data for the given ticker symbol at 5-minute intervals
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="5m")  # Get 5-minute candles for today
        
        if not data.empty:
            # Limit to the most recent 60 candles to ensure we can calculate SMA50
            data = data.tail(60)
            
            # Calculate SMA9, SMA20, and SMA50
            data['SMA9'] = data['Close'].rolling(window=9).mean()
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()

            # Get the last candle (most recent one)
            current_candle = data.iloc[-1]

            # Prepare the response
            response_data = {
                "ticker": ticker,
                "current_close_price": current_candle['Close'],
                "SMA9": current_candle['SMA9'],
                "SMA20": current_candle['SMA20'],
                "SMA50": current_candle['SMA50']
            }

            return Response(response_data)
        else:
            return Response({"error": "No data available for the ticker."}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
