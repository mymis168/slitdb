from datetime import date, timedelta
from pathlib import Path
import sqlite3

import pandas as pd
import yfinance as yf


#保險方式: 透過__file__ 取得目前所在路徑
#DATABASE_PATH = Path(__file__).with_name("stockdb.db")
#透過 .\  (./ ) 指定目前所在目錄亦可
DATABASE_PATH = "./stockdb.db"
PERIODS = ("1d", "5d", "1wk", "2wk", "1mo", "3mo", "6mo", "1y")


def initialize_database() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS stockinfo (
                sid INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                date TEXT,
                open NUMERIC,
                close NUMERIC,
                high NUMERIC,
                low NUMERIC,
                vol INTEGER
            )"""
        )
        columns = {
            row[1] for row in connection.execute("PRAGMA table_info(stockinfo)")
        }
        if "date" not in columns:
            connection.execute("ALTER TABLE stockinfo ADD COLUMN date TEXT")
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_stockinfo_ticker_date "
            "ON stockinfo(ticker, date)"
        )


def fetch_history(ticker: str, period: str) -> pd.DataFrame:
    if period not in PERIODS:
        raise ValueError(f"不支援的資料區間：{period}")

    symbol = ticker.strip().upper()
    if period in ("1wk", "2wk"):
        days = 7 if period == "1wk" else 14
        end = date.today() + timedelta(days=1)
        start = end - timedelta(days=days)
        return yf.Ticker(symbol).history(
            start=start.isoformat(),
            end=end.isoformat(),
            interval="1d",
            auto_adjust=False,
            timeout=20,
        )

    return yf.Ticker(symbol).history(
        period=period,
        interval="1d",
        auto_adjust=False,
        timeout=20,
    )


def _number(value: object) -> float | None:
    if pd.isna(value):
        return None
    return float(value)


def save_history(ticker: str, history: pd.DataFrame) -> int:
    symbol = ticker.strip().upper()
    records = []
    for timestamp, row in history.iterrows():
        volume = _number(row.get("Volume"))
        records.append(
            (
                symbol,
                pd.Timestamp(timestamp).date().isoformat(),
                _number(row.get("Open")),
                _number(row.get("Close")),
                _number(row.get("High")),
                _number(row.get("Low")),
                int(volume) if volume is not None else None,
            )
        )

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.executemany(
            """INSERT OR REPLACE INTO stockinfo
               (ticker, date, open, close, high, low, vol)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            records,
        )
    return cursor.rowcount


def list_tickers() -> list[str]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            "SELECT DISTINCT ticker FROM stockinfo "
            "WHERE date IS NOT NULL ORDER BY ticker"
        ).fetchall()
    return [row[0] for row in rows]


def load_history(ticker: str) -> pd.DataFrame:
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(
            """SELECT date, open, close, high, low, vol
               FROM stockinfo
               WHERE ticker = ? AND date IS NOT NULL
               ORDER BY date""",
            connection,
            params=(ticker,),
        )