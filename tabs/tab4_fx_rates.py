import streamlit as st

def show_fx_rates(fx_data):
    st.header("FX & Rates")

    fx_close = fx_data["Close"].copy()
    normalized_fx_close = fx_close / fx_close.iloc[0] * 100

    st.subheader("FX Market Performance (Base 100)")
    st.line_chart(normalized_fx_close, x_label="Date", y_label="Indexed FX Rate (Base 100)")

    st.subheader("FX Exposure & P&L")

    col1, col2 = st.columns(2)

    with col1:
        # Currency pair selection
        selected_pair = st.selectbox(
            "Select Currency Pair",
            ["EURUSD=X", "USDJPY=X", "USDSGD=X"]
        )

        # Notional amount
        notional = st.number_input(
            "Enter Notional Amount",
            min_value=0.0,
            value=1000000.0,
            step=1.0
        )

    with col2:
        # Entry FX rate
        default_entry_rate = float(fx_close[selected_pair].iloc[0])
        entry_rate = st.number_input(
            "Enter FX Rate",
            min_value=0.00001,
            value=default_entry_rate,
            step=0.0001,
            format="%.4f",
            key=f"entry_rate_{selected_pair}"
        )
        # Position direction
        position_direction = st.segmented_control(
            "Select Position Direction",
            ["Long", "Short"],
            default="Long"
        )

    metric1, metric2, metric3 = st.columns(3)
    with metric1:
        current_fx_rate = fx_close[selected_pair].iloc[-1]

        st.metric(
            "Current FX Rate",
            f"{current_fx_rate:.4f}"
        )
    with metric2:
        # Unrealized P&L
        if position_direction == "Long":
            unrealized_pnl = (
                    notional * (current_fx_rate - entry_rate)
            )
        else:
            unrealized_pnl = (
                    notional * (entry_rate - current_fx_rate)
            )
        quote_currency = selected_pair[3:6]
        st.metric(
            "Unrealized P&L",
            f"{unrealized_pnl:,.2f} {quote_currency}"
        )
    with metric3:
        # Position return
        if notional > 0.0 and entry_rate > 0.0:
            position_return = (unrealized_pnl
                               / (notional * entry_rate)
                               * 100
                               )
        else:
            position_return = 0.0

        st.metric(
            "Position Return",
            f"{position_return:+,.2f}%"
        )

    # FX Shock
    st.divider()
    st.subheader("FX Stress Test")
    fx_shock = st.slider(
        "FX Shock (%)",
        min_value=-5.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )
    col1, col2 = st.columns(2)
    with col1:
        stressed_fx_rate = (
                current_fx_rate * (1 + fx_shock / 100)
        )
        st.metric(
            "Stressed FX Rate",
            f"{stressed_fx_rate:.4f}"
        )

    # Stressed P&L
    with col2:
        if position_direction == "Long":
            stressed_pnl = (
                    notional * (stressed_fx_rate - entry_rate)
            )
        else:
            stressed_pnl = (
                    notional * (entry_rate - stressed_fx_rate)
            )

        # P&L Impact
        pnl_impact = stressed_pnl - unrealized_pnl

        # Display Stressed P&L
        st.metric(
            "Stressed P&L",
            f"{stressed_pnl:,.2f} {quote_currency}",
            delta=f"{pnl_impact:+,.2f} {quote_currency}"
        )


