# 股票行情資料庫

以 Streamlit 建立的個股行情下載與趨勢檢視工具。行情由 Yahoo Finance 提供，並儲存在專案根目錄的 `stockdb.db`。

## 啟動

```powershell
uv sync
uv run streamlit run Streamlit_app.py
```

「下載股票資料」頁面可輸入代號（例如 `AAPL` 或 `2330.TW`）並選擇區間；「股價趨勢」頁面可選擇已儲存的股票查看收盤價走勢。
