import streamlit as st

st.set_page_config(page_title="Buy & Hold Investment Calculator", layout="centered")

st.title("🏠 Buy & Hold Real Estate Calculator")

st.markdown("Analyze rental cash flow, cash-on-cash return, and long-term projections.")

# -------------------------------
# PURCHASE DETAILS
# -------------------------------
st.header("Purchase Details")

purchase_price = st.number_input("Purchase Price ($)", value=250000)
down_payment_percent = st.slider("Down Payment (%)", 0.0, 50.0, 20.0)
interest_rate = st.number_input("Interest Rate (%)", value=6.5)
loan_term_years = st.selectbox("Loan Term (Years)", [15, 20, 25, 30])

down_payment = purchase_price * (down_payment_percent / 100)
loan_amount = purchase_price - down_payment

# Monthly mortgage formula
monthly_rate = (interest_rate / 100) / 12
num_payments = loan_term_years * 12
monthly_mortgage = (
    loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments)
    / ((1 + monthly_rate) ** num_payments - 1)
)

# -------------------------------
# INCOME
# -------------------------------
st.header("Rental Income")

monthly_rent = st.number_input("Monthly Rent ($)", value=2000)
rent_growth = st.slider("Annual Rent Growth (%)", 0.0, 10.0, 3.0)

# -------------------------------
# EXPENSES
# -------------------------------
st.header("Expenses (Monthly)")

taxes = st.number_input("Property Taxes", value=250)
insurance = st.number_input("Insurance", value=120)
maintenance = st.number_input("Maintenance", value=150)
vacancy = st.number_input("Vacancy Allowance", value=100)
property_management = st.number_input("Property Management", value=0)

total_monthly_expenses = (
    monthly_mortgage +
    taxes +
    insurance +
    maintenance +
    vacancy +
    property_management
)

# -------------------------------
# CASH FLOW
# -------------------------------
st.header("Cash Flow")

monthly_cash_flow = monthly_rent - total_monthly_expenses
annual_cash_flow = monthly_cash_flow * 12

st.metric("Monthly Cash Flow", f"${monthly_cash_flow:,.2f}")
st.metric("Annual Cash Flow", f"${annual_cash_flow:,.2f}")

# -------------------------------
# CASH ON CASH RETURN
# -------------------------------
st.header("Cash-on-Cash Return")

closing_costs = st.number_input("Estimated Closing Costs ($)", value=5000)
total_cash_invested = down_payment + closing_costs

cash_on_cash = (annual_cash_flow / total_cash_invested) * 100 if total_cash_invested > 0 else 0

st.metric("Total Cash Invested", f"${total_cash_invested:,.2f}")
st.metric("Cash-on-Cash Return", f"{cash_on_cash:.2f}%")

# -------------------------------
# PROJECTIONS
# -------------------------------
st.header("Long-Term Projections")

years = st.slider("Projection Years", 5, 30, 10)
appreciation_rate = st.slider("Annual Appreciation (%)", 0.0, 10.0, 4.0)

future_value = purchase_price * ((1 + appreciation_rate / 100) ** years)
future_rent = monthly_rent * ((1 + rent_growth / 100) ** years)

st.metric("Estimated Property Value", f"${future_value:,.0f}")
st.metric("Projected Monthly Rent", f"${future_rent:,.0f}")

# -------------------------------
# SUMMARY
# -------------------------------
st.success("Investment Snapshot")

st.write(f"""
- **Loan Amount:** ${loan_amount:,.0f}  
- **Monthly Mortgage:** ${monthly_mortgage:,.2f}  
- **Annual Cash Flow:** ${annual_cash_flow:,.2f}  
- **Cash-on-Cash Return:** {cash_on_cash:.2f}%  
- **Projected Value in {years} Years:** ${future_value:,.0f}
""")
