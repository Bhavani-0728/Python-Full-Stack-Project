# frontend/app.py
import streamlit as st
import requests
from datetime import date
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

st.set_page_config(page_title="💰 Expense Tracker", layout="wide")
st.title("💰 Expense Tracker Web App")

# -------------------- Session State --------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

# -------------------- Sidebar --------------------
with st.sidebar:
    st.header("🔐 Login / Register")

    if st.session_state.logged_in and st.session_state.username:
        st.write(f"👤 Logged in as: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.success("Logged out successfully!")
            st.rerun()

    else:
        auth_mode = st.radio("Select Mode", ["Login", "Register"])

        # -------------------- Login --------------------
        if auth_mode == "Login":
            login_user = st.text_input("Email / Username", key="login_user")
            login_pass = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                if not login_user or not login_pass:
                    st.warning("Please fill both fields!")
                else:
                    resp = requests.post(f"{API_URL}/login", json={"username": login_user, "password": login_pass})
                    result = resp.json()
                    if resp.status_code == 200 and result.get("Success"):
                        st.session_state.logged_in = True
                        st.session_state.user_id = result.get("Data", {}).get("id")
                        st.session_state.username = (
                            result.get("Data", {}).get("username")
                            or result.get("Data", {}).get("name")
                            or login_user
                        )
                        st.success(f"Welcome {st.session_state.username}!")
                        st.rerun()
                    else:
                        st.error(result.get("Message", "Login failed. Please register first."))

        # -------------------- Register --------------------
        elif auth_mode == "Register":
            reg_user = st.text_input("Username", key="reg_user")
            reg_email = st.text_input("Email", key="reg_email")
            reg_pass = st.text_input("Password", type="password", key="reg_pass")
            if st.button("Register"):
                if not reg_user or not reg_email or not reg_pass:
                    st.warning("Please fill all fields!")
                else:
                    resp = requests.post(f"{API_URL}/register", json={
                        "username": reg_user,
                        "email": reg_email,
                        "password": reg_pass
                    })
                    if resp.status_code == 200 and resp.json().get("Success"):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error(resp.json().get("Message", "Registration failed."))

# -------------------- Main Page --------------------
if st.session_state.logged_in:
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
                        st.success(resp.json().get("Message"))
                    else:
                        st.warning("Please enter a username!")

        st.subheader("All Profiles")
        if st.button("Load Profiles", key="load_profiles"):
            resp = requests.get(f"{API_URL}/profiles")
            profiles = resp.json().get("Data", [])
            st.table(profiles if profiles else [])

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
                    "type_": type_,  # fixed key
                    "date": str(txn_date),
                    "amount": amount,
                    "description": description
                }
                resp = requests.post(f"{API_URL}/transactions", json=data)
                st.success(resp.json().get("Message"))

        st.subheader("View Transactions")
        view_user_id = st.number_input("User ID to View Transactions", min_value=1, key="view_txn_user")
        if st.button("Load Transactions", key="load_txns"):
            resp = requests.get(f"{API_URL}/transactions/{view_user_id}")
            transactions = resp.json().get("Data", [])
            if transactions:
                st.table(transactions)
            else:
                st.info("No transactions found.")

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
                st.success(resp.json().get("Message"))

        st.subheader("View Budget")
        view_budget_user = st.number_input("User ID to View Budget", min_value=1, key="view_budget_user")
        if st.button("Load Budget", key="load_budget"):
            resp = requests.get(f"{API_URL}/budgets/{view_budget_user}")
            budgets = resp.json().get("Data", [])
            st.table(budgets if budgets else [])

    # -------------------- Dashboard Tab --------------------
    with tab4:
        st.header("📈 Dashboard - Spending Insights")
        dashboard_user_id = st.number_input("Select User ID for Dashboard", min_value=1, key="dashboard_user")
        if st.button("Load Dashboard"):
            resp = requests.get(f"{API_URL}/transactions/{dashboard_user_id}")
            transactions = resp.json().get("Data", [])
            if not transactions:
                st.info("No transactions available for this user.")
            else:
                df = pd.DataFrame(transactions)
                df['date'] = pd.to_datetime(df['date'])
                expenses = df[df['type'] == 'Expense']  # <-- use 'type', not 'type_'


                # Category Breakdown Chart
                category_totals = expenses.groupby('category')['amount'].sum().reset_index()
                fig_cat = px.pie(category_totals, values='amount', names='category', title="Expenses by Category")
                st.plotly_chart(fig_cat, use_container_width=True)


                # Monthly Spending Chart
                expenses['month'] = expenses['date'].dt.to_period('M')  # get year-month period
                monthly_totals = expenses.groupby('month')['amount'].sum().reset_index()
                monthly_totals['month'] = monthly_totals['month'].astype(str)  # convert to 'YYYY-MM' string

                fig_month = px.bar(
                    monthly_totals,
                    x='month',
                    y='amount',
                    title="Monthly Expenses",
                    color='amount',
                    labels={'month': 'Month', 'amount': 'Total Spent'}
                )
                st.plotly_chart(fig_month, use_container_width=True)

else:
    st.write("🔑 Please click Login or Register in the sidebar to access the Expense Tracker.")
