import streamlit as st
import pandas as pd
import ta 
import matplotlib.pyplot as plt 

# Streamlit Page Config
st.set_page_config(page_title="NQ Trading Dashboard", layout="wide")

# Title
st.title("📈 Nasdaq-100 (NQ) Trading Dashboard")

# Fetch NQ data
@st.cache_data
def get_nq_data():
    nq = yf.download('NQ=F', period='1d', interval='1m')  # Last day, 1-minute intervals
    nq['SMA_50'] = ta.trend.sma_indicator(nq['Close'], window=50)
    nq['SMA_200'] = ta.trend.sma_indicator(nq['Close'], window=200)
    nq['RSI'] = ta.momentum.rsi(nq['Close'], window=14)
    
    # Signal Logic
    nq['Signal'] = 'Neutral'
    nq.loc[(nq['Close'] > nq['SMA_50']) & (nq['RSI'] < 30), 'Signal'] = 'Long'
    nq.loc[(nq['Close'] < nq['SMA_50']) & (nq['RSI'] > 70), 'Signal'] = 'Short'
    
    return nq

nq_data = get_nq_data()

# Latest Price
st.subheader("📊 Latest Price & Signal")
latest_price = nq_data['Close'].iloc[-1]
latest_signal = nq_data['Signal'].iloc[-1]
st.metric(label="NQ Latest Price", value=f"${latest_price:.2f}")
st.metric(label="Trade Signal", value=latest_signal)

# Chart
st.subheader("📉 Historical Data with Signals")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(nq_data.index, nq_data['Close'], label="Close Price", color='blue', linewidth=1)
ax.plot(nq_data.index, nq_data['SMA_50'], label="SMA 50", color='green', linestyle='dashed')
ax.plot(nq_data.index, nq_data['SMA_200'], label="SMA 200", color='red', linestyle='dashed')

# Mark buy/sell points
buy_signals = nq_data[nq_data['Signal'] == 'Long']
sell_signals = nq_data[nq_data['Signal'] == 'Short']
ax.scatter(buy_signals.index, buy_signals['Close'], label="Buy Signal", marker='^', color='green', alpha=1, s=100)
ax.scatter(sell_signals.index, sell_signals['Close'], label="Sell Signal", marker='v', color='red', alpha=1, s=100)

ax.legend()
ax.set_title("NQ Price with Trading Signals")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
st.pyplot(fig)

# Show Data
st.subheader("📝 Data Table")
st.dataframe(nq_data[['Close', 'SMA_50', 'SMA_200', 'RSI', 'Signal']].tail(10))

