# dashboard.py
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
from pypfopt import expected_returns, risk_models, EfficientFrontier
from calculation import get_asset_prices

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="Investment Dashboard", layout="wide")
st.title("💰 Investment Dashboard - Vietnam & Global Assets")
st.write("Track performance, see alerts, and get portfolio suggestions.")

# ----------------------------
# User Inputs
# ----------------------------
st.sidebar.header("Settings")

period = st.sidebar.selectbox("Select period for price data:", ["6mo", "1y", "2y", "5y"], index=1)
alert_threshold = st.sidebar.slider("Alert threshold for drops (%)", 1, 50, 10)

# ----------------------------
# Fetch Price Data
# ----------------------------
st.subheader("📈 Historical Price Data")

data = get_asset_prices(period=period)
if not data.empty:
    st.line_chart(data)
else:
    st.warning("No price data available.")

# ----------------------------
# Alerts for Investment Opportunities
# ----------------------------
st.subheader("⚠️ Price Drop Alerts")

if not data.empty:
    pct_change = data.pct_change().dropna()
    alerts = {}
    for asset in pct_change.columns:
        if (pct_change[asset] * 100).min() <= -alert_threshold:
            drop = round(pct_change[asset].min() * 100, 2)
            alerts[asset] = f"Dropped {drop}% - Potential buy opportunity!"

    if alerts:
        for asset, msg in alerts.items():
            st.warning(f"{asset}: {msg}")
    else:
        st.info("No significant drops detected.")

# ----------------------------
# Portfolio Optimization
# ----------------------------
st.subheader("💡 Portfolio Allocation Suggestion")

if not data.empty:
    try:
        mu = expected_returns.mean_historical_return(data)
        S = risk_models.sample_cov(data)

        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        st.write("**Optimal Portfolio Allocation (Max Sharpe Ratio):**")
        st.write(cleaned_weights)

        performance = ef.portfolio_performance(verbose=True)
        st.write(f"Expected annual return: {performance[0]*100:.2f}%")
        st.write(f"Annual volatility: {performance[1]*100:.2f}%")
        st.write(f"Sharpe Ratio: {performance[2]:.2f}")

    except Exception as e:
        st.warning(f"Could not optimize portfolio: {e}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Created by Vu Manh Dat - Powered by Streamlit, Yahoo Finance & PyPortfolioOpt")
