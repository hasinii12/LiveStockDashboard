import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Live Stock Dashboard", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📈 Live Stock Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Live stock analysis with returns & volatility</p>",
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Select Options")

ticker = st.sidebar.selectbox(
    "Choose Stock",
    ["AAPL", "MSFT", "NVDA", "GOOGL", "TSLA"]
)

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y"]
)

# -----------------------------
# Fetch data
# -----------------------------
stock = yf.Ticker(ticker)
data = stock.history(period=period)

data = data.reset_index()
data = data[['Date', 'Close', 'Volume']]

# -----------------------------
# Feature engineering
# -----------------------------
data['Daily Return (%)'] = data['Close'].pct_change() * 100
data['Cumulative Return (%)'] = (1 + data['Daily Return (%)']/100).cumprod() * 100
data['Volatility (7D)'] = data['Daily Return (%)'].rolling(window=7).std()

# -----------------------------
# KPI Metrics
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Latest Price", f"${data['Close'].iloc[-1]:.2f}")
col2.metric("Highest Price", f"${data['Close'].max():.2f}")
col3.metric("Lowest Price", f"${data['Close'].min():.2f}")

# -----------------------------
# Price Trend Plot
# -----------------------------
st.subheader("📈 Stock Price Trend")

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(data['Date'], data['Close'], label="Close Price")
ax1.set_xlabel("Date")
ax1.set_ylabel("Price")
ax1.set_title(f"{ticker} Price Trend")

ax1.tick_params(axis='x', rotation=45)
ax1.legend()
plt.tight_layout()

st.pyplot(fig1)

# -----------------------------
# Cumulative Return Plot
# -----------------------------
st.subheader("📊 Cumulative Return")

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(data['Date'], data['Cumulative Return (%)'])
ax2.set_xlabel("Date")
ax2.set_ylabel("Cumulative Return (%)")
ax2.set_title("Cumulative Return Over Time")

ax2.tick_params(axis='x', rotation=45)
plt.tight_layout()

st.pyplot(fig2)

# -----------------------------
# Volatility Plot
# -----------------------------
st.subheader("📉 7-Day Rolling Volatility")

fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(data['Date'], data['Volatility (7D)'])
ax3.set_xlabel("Date")
ax3.set_ylabel("Volatility (%)")
ax3.set_title("7-Day Rolling Volatility")

ax3.tick_params(axis='x', rotation=45)
plt.tight_layout()

st.pyplot(fig3)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("📄 Data Preview")
st.dataframe(data.tail(10))

# -----------------------------
# Insights
# -----------------------------
st.subheader("🧠 Insights")

if data['Close'].iloc[-1] > data['Close'].mean():
    st.success("The stock is trading above its average price → Bullish trend")
else:
    st.warning("The stock is trading below its average price → Bearish trend")
