import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Buy & Hold Analyzer", layout="wide")

st.title("🏠 Buy & Hold Real Estate Investment Analyzer")
st.caption("Cash Flow • Cash-on-Cash • Equity • Projections")

# =================================
# INPUTS
# =================================
st.sidebar.header("Property Inputs")

purchase_price = st.sidebar.number_input("Purchase Price ($)", 50000, 5000000, 250000)
down_pct = st.sidebar.slider("Down Payment (%)", 0.0, 50.0, 20.0)
interest_rate = st.sidebar.number_input("Interest Rate (%)", 1.0, 15.0, 6.5)
loan_years = st.sidebar.selectbox("Loan Term (Years)", [15, 20, 25, 30])

monthly_rent = st.sidebar.number_input("Monthly Rent ($)", 500, 20000, 2000)
rent_growth = st.sidebar.slider("Annual Rent Growth (%)", 0.0, 10.0, 3.0)

expense_ratio = st.sidebar.slider("Operating Expense Ratio (%)", 10.0, 60.0, 35.0)

appreciation = st.sidebar.slider("Annual Appreciation (%)", 0.0, 10.0, 4.0)
projection_years = st.sidebar.slider("Projection Years", 5, 30, 10)

closing_costs = st.sidebar.number_input("Closing Costs ($)", 0, 50000, 5000)

# =================================
# CALCULATIONS
# =================================
down_payment = purchase_price * (down_pct / 100)
loan_amount = purchase_price - down_payment

monthly_rate = (interest_rate / 100) / 12
payments = loan_years * 12

monthly_mortgage = loan_amount * (
    monthly_rate * (1 + monthly_rate) ** payments
) / ((1 + monthly_rate) ** payments - 1)

annual_rent = monthly_rent * 12
annual_expenses = annual_rent * (expense_ratio / 100)
noi = annual_rent - annual_expenses
annual_debt = monthly_mortgage * 12

annual_cash_flow = noi - annual_debt
monthly_cash_flow = annual_cash_flow / 12

cash_invested = down_payment + closing_costs
cash_on_cash = (annual_cash_flow / cash_invested) * 100 if cash_invested else 0
cap_rate = (noi / purchase_price) * 100
dscr = noi / annual_debt if annual_debt else 0

# =================================
# METRICS
# =================================
st.header("📊 Investment Performance")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Monthly Cash Flow", f"${monthly_cash_flow:,.0f}")
col2.metric("Annual Cash Flow", f"${annual_cash_flow:,.0f}")
col3.metric("Cash-on-Cash Return", f"{cash_on_cash:.2f}%")
col4.metric("Cap Rate", f"{cap_rate:.2f}%")

col5, col6, col7 = st.columns(3)
col5.metric("NOI", f"${noi:,.0f}")
col6.metric("DSCR", f"{dscr:.2f}")
col7.metric("Cash Invested", f"${cash_invested:,.0f}")

# =================================
# PROJECTIONS TABLE
# =================================
st.header("📈 Long-Term Projections")

projection_data = []

value = purchase_price
rent = annual_rent
loan_balance = loan_amount

for year in range(1, projection_years + 1):
    value *= (1 + appreciation / 100)
    rent *= (1 + rent_growth / 100)
    expenses = rent * (expense_ratio / 100)
    noi_year = rent - expenses
    equity = value - loan_balance

    projection_data.append([
        year,
        round(value),
        round(rent),
        round(noi_year),
        round(equity)
    ])

df = pd.DataFrame(
    projection_data,
    columns=["Year", "Property Value", "Annual Rent", "NOI", "Equity"]
)

st.dataframe(df, use_container_width=True)

# =================================
# CHARTS
# =================================
st.header("📉 Visual Analysis")

fig, ax = plt.subplots()
ax.plot(df["Year"], df["Equity"])
ax.set_title("Equity Growth Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Equity ($)")
st.pyplot(fig)

fig2, ax2 = plt.subplots()
ax2.plot(df["Year"], df["NOI"])
ax2.set_title("NOI Growth Over Time")
ax2.set_xlabel("Year")
ax2.set_ylabel("NOI ($)")
st.pyplot(fig2)

# =================================
# SUMMARY
# =================================
st.success("📌 Investment Summary")

st.markdown(f"""
**Purchase Price:** ${purchase_price:,.0f}  
**Loan Amount:** ${loan_amount:,.0f}  
**Monthly Mortgage:** ${monthly_mortgage:,.0f}  

**Annual Cash Flow:** ${annual_cash_flow:,.0f}  
**Cash-on-Cash Return:** {cash_on_cash:.2f}%  
**Projected Value in {projection_years} Years:** ${df.iloc[-1]['Property Value']:,.0f}  
**Projected Equity:** ${df.iloc[-1]['Equity']:,.0f}
""")
