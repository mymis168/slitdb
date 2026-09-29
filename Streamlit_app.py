import streamlit as st


st.set_page_config(page_title="股票行情資料庫", page_icon=":material/query_stats:")

page = st.navigation(
    [
        st.Page(
            "ticker_parser.py",
            title="下載股票資料",
            icon=":material/download:",
        ),
        st.Page(
            "analyse.py",
            title="股價趨勢",
            icon=":material/show_chart:",
        ),
    ]
)
page.run()