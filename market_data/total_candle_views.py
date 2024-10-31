# market_data/total_candle_views.py
import yfinance as yf
from rest_framework.decorators import api_view
from rest_framework.response import Response


# This is for checking candle fetch or not
@api_view(['GET'])
def get_nse_5min_candles(request, ticker):
    try:
        # Fetch stock data for the given ticker symbol at 5-minute intervals for the last 5 days
        stock = yf.Ticker(ticker)
        data = stock.history(period="5d", interval="5m")

        if not data.empty:
            # Select relevant columns: Datetime, Open, High, Low, Close
            data = data[['Open', 'High', 'Low', 'Close']]
            data.reset_index(inplace=True)  # Reset index to make Datetime a column
            
            # Format datetime and convert data to a list of dictionaries
            candles = [
                {
                    "Datetime": row['Datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                    "Open": row['Open'],
                    "High": row['High'],
                    "Low": row['Low'],
                    "Close": row['Close']
                }
                for _, row in data.iterrows()
            ]
            
            # Prepare response data
            response_data = {
                "ticker": ticker,
                "total_candles_fetched": len(candles),
                "candles": candles
            }

            return Response(response_data)
        else:
            return Response({"error": "No data available for the ticker."}, status=404)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)
