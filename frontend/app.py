# frontend/app.py
import streamlit as st
import requests
from datetime import date
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.set_page_config(page_title="💰 Expense Tracker", layout="wide")
st.title("💰 Expense Tracker Web App")

# -------------------- TABS --------------------
tab1, tab2, tab3, tab4 = st.tabs(["👤 Profiles", "💸 Transactions", "📊 Budget", "📈 Dashboard"])

# -------------------- Profiles Tab --------------------
with tab1:
    st.header("👤 Profiles Management")
    with st.expander("➕ Add New Profile"):
        col1, col2 = st.columns([3, 1])
        with col1:
            username = st.text_input("Enter Username", key="add_profile")
        with col2:
            if st.button("Add Profile"):
                if username:
                    resp = requests.post(f"{API_URL}/profiles", json={"username": username})
                    if resp.status_code == 200:
                        st.success(resp.json().get("Message"))
                    else:
                        st.error("Failed to add profile.")
                else:
                    st.warning("Please enter a username!")

    st.subheader("All Profiles")
    if st.button("Load Profiles", key="load_profiles"):
        resp = requests.get(f"{API_URL}/profiles")
        if resp.status_code == 200:
            profiles = resp.json().get("Data", [])
            st.table(profiles if profiles else [])
        else:
            st.error("Failed to fetch profiles.")

# -------------------- Transactions Tab --------------------
with tab2:
    st.header("💸 Transactions Management")
    with st.expander("➕ Add Transaction"):
        col1, col2 = st.columns(2)
        with col1:
            user_id_txn = st.number_input("User ID", min_value=1, key="txn_user")
            category = st.text_input("Category", key="txn_category")
            type_ = st.selectbox("Type", ["Expense", "Income"], key="txn_type")
        with col2:
            txn_date = st.date_input("Date", value=date.today(), key="txn_date")
            amount = st.number_input("Amount", min_value=0.0, key="txn_amount")
            description = st.text_input("Description", key="txn_desc")

        if st.button("Add Transaction"):
            data = {
                "user_id": user_id_txn,
                "category": category,
                "type": type_,  # ✅ backend expects "type"
                "date": str(txn_date),
                "amount": amount,
                "description": description
            }
            resp = requests.post(f"{API_URL}/transactions", json=data)
            if resp.status_code == 200:
                st.success(resp.json().get("Message"))
            else:
                st.error("Failed to add transaction.")

    st.subheader("View Transactions")
    view_user_id = st.number_input("User ID to View Transactions", min_value=1, key="view_txn_user")
    if st.button("Load Transactions", key="load_txns"):
        resp = requests.get(f"{API_URL}/transactions/{view_user_id}")
        if resp.status_code == 200:
            transactions = resp.json().get("Data", [])
            if transactions:
                st.table(transactions)
            else:
                st.info("No transactions found.")
        else:
            st.error("Failed to fetch transactions.")

# -------------------- Budget Tab --------------------
with tab3:
    st.header("📊 Budget Management")
    with st.expander("➕ Set Budget"):
        col1, col2 = st.columns(2)
        with col1:
            budget_user_id = st.number_input("User ID", min_value=1, key="budget_user")
        with col2:
            budget_amount = st.number_input("Budget Amount", min_value=0.0, key="budget_amount")

        if st.button("Set Budget"):
            resp = requests.post(f"{API_URL}/budgets", json={"user_id": budget_user_id, "budget": budget_amount})
            if resp.status_code == 200:
                st.success(resp.json().get("Message"))
            else:
                st.error("Failed to set budget.")

    st.subheader("View Budget")
    view_budget_user = st.number_input("User ID to View Budget", min_value=1, key="view_budget_user")
    if st.button("Load Budget", key="load_budget"):
        resp = requests.get(f"{API_URL}/budgets/{view_budget_user}")
        if resp.status_code == 200:
            budgets = resp.json().get("Data", [])
            st.table(budgets if budgets else [])
        else:
            st.error("Failed to fetch budget.")

# -------------------- Dashboard Tab --------------------
with tab4:
    st.header("📈 Dashboard - Spending Insights")
    dashboard_user_id = st.number_input("Select User ID for Dashboard", min_value=1, key="dashboard_user")

    if st.button("Load Dashboard"):
        resp = requests.get(f"{API_URL}/transactions/{dashboard_user_id}")
        if resp.status_code == 200:
            transactions = resp.json().get("Data", [])
            if not transactions:
                st.info("No transactions available for this user.")
            else:
                df = pd.DataFrame(transactions)
                df['date'] = pd.to_datetime(df['date'])

                # Filter only Expenses for charts
                expenses = df[df['type'].str.lower() == 'expense']

                # ---- Monthly Spending Chart ----
                expenses['month'] = expenses['date'].dt.to_period('M')
                monthly_totals = expenses.groupby('month')['amount'].sum().reset_index()
                monthly_totals['month'] = monthly_totals['month'].astype(str)
                fig_month = px.bar(monthly_totals, x='month', y='amount',
                                   title="Monthly Expenses", color='amount')
                st.plotly_chart(fig_month, use_container_width=True)

                # ---- Category Breakdown Chart ----
                category_totals = expenses.groupby('category')['amount'].sum().reset_index()
                fig_cat = px.pie(category_totals, values='amount', names='category',
                                 title="Expenses by Category")
                st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.error("Failed to fetch dashboard data.")
