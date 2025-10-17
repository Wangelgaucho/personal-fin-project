# calculation.py
# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd

# ----------------------------
# Define Assets
# ----------------------------
ASSETS = {
    "VNM_Fund": "FUEVFVND.VN",  # Vietnam ETF
    "Gold": "GC=F",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "US_Bond": "IEF"  # US Bond ETF
}

# ----------------------------
# Function to get asset prices
# ----------------------------
def get_asset_prices(period="6mo", interval="1d"):
    """
    Download price data for all defined assets.
    Returns a DataFrame with tickers as columns.
    """
    tickers = list(ASSETS.values())
    try:
        data = yf.download(tickers, period=period, interval=interval, auto_adjust=True)
        
        # Check for column structure
        if "Close" in data.columns:
            data = data["Close"]
        elif "Adj Close" in data.columns:
            data = data["Adj Close"]
        else:
            # MultiIndex fallback if multiple tickers
            if isinstance(data.columns, pd.MultiIndex):
                data = data['Close']
        
        data = data.ffill().bfill()  # fill missing data
        data.rename(columns={v: k for k, v in ASSETS.items()}, inplace=True)
        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return pd.DataFrame()
