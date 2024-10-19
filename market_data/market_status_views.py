# market_data/market_status_views.py
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def is_market_open(request, ticker="^NSEI"):
    try:
        # Get ticker data for the given symbol at 1-minute intervals (real-time)
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")
        
        # Check if any data is returned
        if data.empty:
            return Response({"ticker": ticker, "market_status": "closed", "reason": "No data available"}, status=200)

        # Get the last timestamp from the data
        last_timestamp = data.index[-1]

        # Get current time in IST (Indian Standard Time)
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist)

        # Check if the last timestamp is within the last 15 minutes
        if current_time - last_timestamp <= timedelta(minutes=15):
            return Response({"ticker": ticker, "market_status": "open", "last_updated": last_timestamp.strftime('%Y-%m-%d %H:%M:%S')}, status=200)
        else:
            return Response({"ticker": ticker, "market_status": "closed", "last_updated": last_timestamp.strftime('%Y-%m-%d %H:%M:%S')}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
