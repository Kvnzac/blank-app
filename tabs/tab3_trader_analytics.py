import streamlit as st
import pandas as pd

def show_trader_analytics(trader_data):
    st.header("Trader Analytics")

    # --------------------------------------------------------
    # 3. Trader Yearly Commissions
    # --------------------------------------------------------

    st.subheader("Trader Yearly Commissions")

    commission_rate = 0.02
    minimum_return = 1.0

    # Aggregate annual results by trader
    trader_annual_df = trader_data.groupby(
        ["trader", "year"]
    )[["trade_results", "notional_usd"]].sum()

    # Calculate annual returns
    trader_annual_df["pnl_to_notional_pct"] = (
        trader_annual_df["trade_results"]
        / trader_annual_df["notional_usd"]
    ) * 100

    # Calculate commissions for eligible traders
    trader_annual_df["commission"] = (
        trader_annual_df["trade_results"] * commission_rate
    ).where(
        trader_annual_df["pnl_to_notional_pct"] > minimum_return,
        0
    )

    # Trader selection
    selected_trader = st.selectbox(
        "Select a trader",
        trader_annual_df.index
        .get_level_values("trader")
        .unique()
    )

    # Display selected trader's annual performance
    st.dataframe(
        trader_annual_df.loc[selected_trader],
        column_config={
            "trade_results": st.column_config.NumberColumn(
                "Annual P&L ($)",
                format="$%.2f"
            ),
            "notional_usd": st.column_config.NumberColumn(
                "Notional ($)",
                format="$%.0f"
            ),
            "pnl_to_notional_pct": st.column_config.NumberColumn(
                "P&L / Notional (%)",
                format="%.2f%%"
            ),
            "commission": st.column_config.NumberColumn(
                "Commission ($)",
                format="$%.2f"
            )
        },
        width="stretch"
    )

    trader_daily_pnl = (
        trader_data.groupby(["trader", pd.Grouper(freq="D")])["trade_results"].agg("sum")
    )
    trader_cumulative_pnl = (
        trader_daily_pnl
        .sort_index(ascending=True)
        .groupby(level="trader")
        .cumsum()
    )

    trader_pnl_chart = (
        trader_cumulative_pnl
        .unstack(level="trader")
        .sort_index()
        .ffill()
        .fillna(0)
    )

    # Trader selection
    compared_traders = st.multiselect(
        "Traders to compare",
        options=trader_pnl_chart.columns,
        default=trader_pnl_chart.columns.tolist()
    )
    filtered_trader_pnl = trader_pnl_chart[compared_traders]

    st.subheader("Trader Cumulative Realized P&L")
    st.line_chart(
        filtered_trader_pnl,
        x_label="Date",
        y_label="Cumulative Realized P&L ($)"
    )

