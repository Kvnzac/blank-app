
import streamlit as st
import pandas as pd
import yfinance as yf
from tabs.tab4_fx_rates import show_fx_rates
from tabs.tab3_trader_analytics import show_trader_analytics
from tabs.tab2_risk_analytics import show_risk_analytics
from tabs.tab1_desk_overview import desk_overview
# ============================================================
# 1. DASHBOARD CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Trading Desk Dashboard",
    layout="wide"
)

st.title("Trading Desk Dashboard")

tab1, tab2, tab3, tab4 = st.tabs([
    "Desk Overview",
    "Risk Analytics",
    "Trader Analytics",
    "FX & Rates"
])


# ============================================================
# 2. DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    spy_data = yf.download(
        "SPY",
        start="2023-01-03",
        end="2025-12-31",
        interval="1d",
        auto_adjust=True
    )

    fx_data = yf.download(
        ["EURUSD=X","USDSGD=X","USDJPY=X"],
        start="2023-01-03",
        end="2025-12-31",
        interval="1d",
        auto_adjust=True
    )

    trades = pd.read_csv(
        "desk_trades.csv",
        parse_dates=["exit_date"],
        index_col="exit_date"
    )

    trades.sort_index(inplace=True)

    return spy_data, fx_data, trades


spy_data, fx_data, df = load_data()


# ============================================================
# 3. DATA PREPARATION
# ============================================================

# Calculate P&L for each trade
df["trade_results"] = (
    (df["exit_price"] - df["entry_price"])
    / df["entry_price"]
) * df["notional_usd"]

# Extract month and year
df["month"] = df.index.to_period("M")
df["year"] = df.index.year

monthly_df = df.groupby("month")[
    ["trade_results", "notional_usd"]
].sum()

monthly_df["trade_returns"] = (
    monthly_df["trade_results"]
    / monthly_df["notional_usd"]
) * 100

# ============================================================
# TAB 1 — DESK OVERVIEW
# ============================================================

with tab1:
    desk_overview(monthly_df, spy_data)

# ============================================================
# TAB 2 — RISK ANALYTICS
# ============================================================

with tab2:
    show_risk_analytics(monthly_df)

# ============================================================
# TAB 3 — TRADER ANALYTICS
# ============================================================

with tab3:
    show_trader_analytics(df)

# ============================================================
# TAB 4 — FX & Rates
# ============================================================

with tab4:
    show_fx_rates(fx_data)


