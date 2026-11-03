import pandas as pd
import streamlit as st

def desk_overview(monthly_df, spy_data):
    monthly_df = monthly_df.copy()
    # --------------------------------------------------------
    # 1. Monthly Desk Returns vs SPY Returns
    # --------------------------------------------------------

    st.header("Monthly Desk Returns vs SPY Returns (%)")

    # Calculate monthly SPY returns
    spy_monthly_returns = (
        spy_data["Close"]
        .resample("ME")
        .last()
        .pct_change()
        * 100
    ).squeeze()

    spy_monthly_returns.index = (
        spy_monthly_returns.index.to_period("M")
    )

    # Combine desk and benchmark returns
    returns_comparison = pd.concat(
        [
            spy_monthly_returns.rename("SPY Returns"),
            monthly_df["trade_returns"].rename("Desk Returns")
        ],
        axis=1,
        join="inner"
    )

    returns_comparison.index = (
        returns_comparison.index.astype(str)
    )

    # Display monthly returns chart
    st.bar_chart(
        returns_comparison,
        color=["#A8D5BA", "#00543C"]
    )

    # --------------------------------------------------------
    # 2. Desk Capital Growth
    # --------------------------------------------------------

    st.header("Desk Capital Growth ($100,000 Initial Capital)")

    initial_capital = 100_000

    # Compound monthly desk returns
    monthly_df["capital_growth"] = (
        initial_capital
        * (1 + monthly_df["trade_returns"] / 100).cumprod()
    )

    # Convert monthly index to timestamps
    monthly_df.index = monthly_df.index.to_timestamp()

    # Display capital growth chart
    st.line_chart(
        monthly_df,
        y="capital_growth",
        x_label="Month",
        y_label="Capital ($)",
        color="#00543C"
    )



