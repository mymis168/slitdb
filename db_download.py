from pathlib import Path

import streamlit as st

from stock_data import DATABASE_PATH, initialize_database


initialize_database()
database_file = Path(DATABASE_PATH)
database_bytes = database_file.read_bytes()

st.title("下載資料庫")
st.caption(f"目前資料庫：{database_file.name}（{len(database_bytes):,} bytes）")
st.download_button(
    "下載 stockdb.db",
    data=database_bytes,
    file_name="stockdb.db",
    mime="application/vnd.sqlite3",
    type="primary",
    icon=":material/download:",
    on_click="ignore",
)