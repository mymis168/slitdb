import streamlit as st

from stock_data import PERIODS, fetch_history, initialize_database, save_history


initialize_database()

st.title("下載股票資料")
st.caption("從 Yahoo Finance 載入每日行情，並儲存至 stockdb.db。")

with st.form("download_stock_history"):
    ticker = st.text_input("股票代號", placeholder="例如 AAPL 或 2330.TW")
    period = st.selectbox("資料區間", PERIODS, index=4)
    submitted = st.form_submit_button(
        "下載並儲存", type="primary", icon=":material/download:"
    )

if submitted:
    ticker = ticker.strip().upper()
    if not ticker:
        st.error("請輸入股票代號。")
    else:
        try:
            with st.spinner(f"正在載入 {ticker} 行情…"):
                history = fetch_history(ticker, period)
                if history.empty:
                    st.warning("查無行情資料，請確認代號或資料區間。")
                else:
                    saved_count = save_history(ticker, history)
                    st.success(f"已儲存 {ticker} 的 {saved_count} 筆行情資料。")
                    st.dataframe(history.tail(10), hide_index=False)
        except Exception as error:
            st.error(f"下載或儲存失敗：{error}")