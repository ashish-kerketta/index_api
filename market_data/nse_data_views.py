# market_data/nse_5min_views.py
import yfinance as yf
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd

@api_view(['GET'])
def get_nse_data(request, ticker):
    try:
        # Fetch stock data for the given ticker symbol at 5-minute intervals
        stock = yf.Ticker(ticker)
        data = stock.history(period="5d", interval="5m")  # Get 5-minute candles for the last 5 days
        
        if not data.empty:
            # Calculate SMA9, SMA20, and SMA50
            data['SMA9'] = data['Close'].rolling(window=9).mean()
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()

            # Get the last candle (most recent one)
            current_candle = data.iloc[-1]
            
            # Prepare the response with values rounded to two decimal places
            response_data = {
                "ticker": ticker,
                "current_close_price": round(current_candle['Close'], 2) if pd.notna(current_candle['Close']) else None,
                "SMA9": round(current_candle['SMA9'], 2) if pd.notna(current_candle['SMA9']) else None,
                "SMA20": round(current_candle['SMA20'], 2) if pd.notna(current_candle['SMA20']) else None,
                "SMA50": round(current_candle['SMA50'], 2) if pd.notna(current_candle['SMA50']) else None
            }

            return Response(response_data)
        else:
            return Response({"error": "No data available for the ticker."}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)

