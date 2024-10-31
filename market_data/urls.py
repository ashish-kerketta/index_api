# market_data/urls.py

from django.urls import path
from .get_high_low_views import get_high_low  # Import from get_high_low_views
from .total_candle_views import get_nse_5min_candles  # Import from total_candle_views.py
from .nse_data_views import get_nse_data  # Import from nse_5min_views.py 

urlpatterns = [
    path('get_high_low/<str:ticker>/', get_high_low, name='GET-HIGH-LOW'),
    path('nse-5min-candle/<str:ticker>/', get_nse_5min_candles, name='NSE-5MIN-CANDLES'),  # Use the correct import
    path('nse-data/<str:ticker>/', get_nse_data, name='NSE-DATA'),  # New URL for 5-min data
]
