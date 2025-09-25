import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# =================
# PROFILES TABLE 
# =================

# Create Profile
def create_profile(username):
    return supabase.table("profiles").insert({
        "username": username,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

# Get All Profiles
def get_all_profiles():
    return supabase.table("profiles").select("*").order("created_at").execute()

# Get a particular profile
def get_profile(profile_id):
    return supabase.table("profiles").select("*").eq("id", profile_id).single().execute()

# Update profile
def update_profile(profile_id, updates: dict):
    # Better: don't overwrite created_at on update
    updates["updated_at"] = datetime.utcnow().isoformat()
    return supabase.table("profiles").update(updates).eq("id", profile_id).execute()

# Delete profile
def delete_profile(profile_id):
    return supabase.table("profiles").delete().eq("id", profile_id).execute() 


# =====================
# TRANSACTIONS TABLE 
# =====================

# Create transaction
def create_transaction(user_id, category, txn_type, date, amount, description=None):
    return supabase.table("transactions").insert({
        "user_id": user_id,
        "category": category,
        "type": txn_type,  # ✅ safe name
        "date": date,
        "amount": amount,
        "description": description,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

# Get transactions for a user
def get_transactions(user_id):
    return supabase.table("transactions").select("*").eq("user_id", user_id).order("date").execute()

# Update transaction
def update_transaction(transaction_id, updates: dict):
    updates["updated_at"] = datetime.utcnow().isoformat()
    return supabase.table("transactions").update(updates).eq("id", transaction_id).execute()

# Delete transaction
def delete_transaction(transaction_id):
    return supabase.table("transactions").delete().eq("id", transaction_id).execute()


# ====================
# BUDGETS TABLE CRUD
# ====================

# Create budget
def create_budget(user_id, budget):
    return supabase.table("budget").insert({   
        "user_id": user_id,
        "budget": budget,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

# Get budget
def get_budget(user_id):
    return supabase.table("budget").select("*").eq("user_id", user_id).order("created_at").limit(1).execute()

# Update budget
def update_budget(budget_id, new_budget):
    return supabase.table("budget").update({
        "budget": new_budget,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("id", budget_id).execute()

# Delete budget
def delete_budget(budget_id):
    return supabase.table("budget").delete().eq("id", budget_id).execute()

# Get all budgets
def get_all_budgets():
    return supabase.table("budget").select("*").order("created_at").execute()
