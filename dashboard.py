# dashboard.py
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from calculation import get_asset_prices
from pypfopt import expected_returns, risk_models, EfficientFrontier

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="Investment Dashboard", layout="wide")
st.title("💰 Investment Dashboard - Vietnam & Global Assets")
st.write("Track performance and get portfolio suggestions based on price data.")

# ----------------------------
# User Inputs
# ----------------------------
st.sidebar.header("Select period for price data")
period = st.sidebar.selectbox("Select period:", ["6mo", "1y", "2y", "5y"], index=1)

# ----------------------------
# Download Price Data
# ----------------------------
st.subheader("📈 Historical Price Data")
data = get_asset_prices(period=period)

if data.empty:
    st.error("No data available. Please check your tickers or try later.")
else:
    st.line_chart(data)

# ----------------------------
# Portfolio Optimization
# ----------------------------
st.subheader("💡 Portfolio Allocation Suggestion")

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
