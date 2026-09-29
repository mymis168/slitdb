import streamlit as st

from stock_data import initialize_database, list_tickers, load_history


initialize_database()

st.title("個股股價趨勢")

tickers = list_tickers()
if not tickers:
    st.info("目前沒有可分析的行情資料，請先下載股票資料。")
else:
    ticker = st.selectbox("選擇股票", tickers)
    history = load_history(ticker)
    st.line_chart(history, x="date", y="close", x_label="日期", y_label="收盤價")
    st.dataframe(history, hide_index=True)