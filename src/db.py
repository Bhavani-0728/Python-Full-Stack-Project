import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# =================
# PROFILES TABLE 
# =================

# Create Profile
def create_profile(username, email=None, password=None):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() if password else None
    return supabase.table("profiles").insert({
        "username": username,
        "email": email,
        "password": hashed_pw,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

# Get all profiles
def get_all_profiles():
    return supabase.table("profiles").select("*").order("created_at").execute()

# Get a single profile by id
def get_profile(profile_id):
    return supabase.table("profiles").select("*").eq("id", profile_id).single().execute()

# Get profile by username or email
def get_profile_by_username(username):
    return supabase.table("profiles").select("*").eq("username", username).execute()

def get_profile_by_email(email):
    return supabase.table("profiles").select("*").eq("email", email).execute()

# Update profile
def update_profile(profile_id, updates: dict):
    updates["created_at"] = datetime.utcnow().isoformat()
    return supabase.table("profiles").update(updates).eq("id", profile_id).execute()

# Delete profile
def delete_profile(profile_id):
    return supabase.table("profiles").delete().eq("id", profile_id).execute() 

# =====================
# TRANSACTIONS TABLE 
# =====================
def create_transaction(user_id, category, type_, date, amount, description=None):
    return supabase.table("transactions").insert({
        "user_id": user_id,
        "category": category,
        "type": type_,        # <-- DB column is 'type', not 'type_'
        "date": date,
        "amount": amount,
        "description": description,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

def get_transactions(user_id):
    return supabase.table("transactions").select("*").eq("user_id", user_id).order("date").execute()

def update_transaction(transaction_id, updates: dict):
    # map type_ to type before updating DB
    if "type_" in updates:
        updates["type"] = updates.pop("type_")
    updates["created_at"] = datetime.utcnow().isoformat()
    return supabase.table("transactions").update(updates).eq("id", transaction_id).execute()


def delete_transaction(transaction_id):
    return supabase.table("transactions").delete().eq("id", transaction_id).execute()

# ====================
# BUDGET TABLE CRUD
# ====================
def create_budget(user_id, budget):
    return supabase.table("budget").insert({
        "user_id": user_id,
        "budget": budget,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

def get_budget(user_id):
    return supabase.table("budget").select("*").eq("user_id", user_id).order("created_at").limit(1).execute()

def update_budget(budget_id, new_budget):
    return supabase.table("budget").update({
        "budget": new_budget,
        "created_at": datetime.utcnow().isoformat()
    }).eq("id", budget_id).execute()

def delete_budget(budget_id):
    return supabase.table("budget").delete().eq("id", budget_id).execute()
