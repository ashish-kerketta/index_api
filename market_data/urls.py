# market_data/urls.py

from django.urls import path
from . import views  # For views in views.py
from .total_candle_views import get_nse_5min_candles  # Import from total_candle_views.py
from .nse_5min_views import get_nse_5min_data  # Import from nse_5min_views.py
from .market_status_views import is_market_open 

urlpatterns = [
    path('nse-index/<str:ticker>/', views.get_nse_index, name='NSE-INDEX'),
    path('nse-5min-candle/<str:ticker>/', get_nse_5min_candles, name='NSE-5MIN-CANDLES'),  # Use the correct import
    path('nse-5min-data/<str:ticker>/', get_nse_5min_data, name='NSE-5MIN-DATA'),  # New URL for 5-min data
    path('market-status/<str:ticker>/', is_market_open, name='MARKET-STATUS'),
]
