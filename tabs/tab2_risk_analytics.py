import streamlit as st

def show_risk_analytics(monthly_df):
    monthly_df = monthly_df.copy()

    st.header("Risk Analytics")

    col1, col2 = st.columns(2)

    with col1:
        # Annualized Volatility
        monthly_df["monthly_returns"] = (
                monthly_df["trade_returns"].dropna() / 100
        )

        annualized_volatility = (
                monthly_df["monthly_returns"].std() * 12 ** 0.5
        )

        st.metric(
            "Annualized Volatility",
            f"{annualized_volatility:.2%}"
        )

        # Sharpe Ratio
        risk_free_rate = 0.03

        mean_monthly_returns = (
            monthly_df["monthly_returns"].mean()
        )

        monthly_risk_free_rate = (
                (1 + risk_free_rate) ** (1 / 12) - 1
        )

        sharpe_ratio = (
                               (mean_monthly_returns - monthly_risk_free_rate)
                               / monthly_df["monthly_returns"].std()
                       ) * 12 ** 0.5

        st.metric(
            "Sharpe Ratio",
            f"{sharpe_ratio:.2f}"
        )

    with col2:
        # Maximum Drawdown
        monthly_df["cumulative_returns"] = (
                1 + monthly_df["monthly_returns"]
        ).cumprod()

        monthly_df["running_peak"] = (
            monthly_df["cumulative_returns"]
            .cummax()
            .clip(lower=1)
        )

        monthly_df["drawdown"] = (
                monthly_df["cumulative_returns"]
                / monthly_df["running_peak"]
                - 1
        )

        max_drawdown = monthly_df["drawdown"].min()

        st.metric(
            "Max Drawdown",
            f"{max_drawdown:.2%}"
        )

        # Historical VaR
        confidence_level = 0.95

        historical_var = -monthly_df[
            "monthly_returns"
        ].quantile(1 - confidence_level)

        st.metric(
            "Historical VaR (95%)",
            f"{historical_var:.2%}"
        )

    st.subheader("Portfolio Drawdown")

    st.line_chart(
        monthly_df["drawdown"] * 100,
        x_label="Month",
        y_label="Drawdown (%)",
        color='#00543C'
    )