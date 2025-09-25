import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

#load environment variables
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")

supabase=create_client(url,key)

# =================
# PROFILES TABLE 
# =================


#Create Profile
def create_profile(username):
    return supabase.table("Profiles").insert({
        "username": username,
        "created_at": datetime.isoformat()
    }).execute()

#Get All Profiles
def get_all_profiles():
    return supabase.table("Profiles").select("*").order("created_at").execute()

#Get a particular profile
def get_profile(profile_id):
    return supabase.table("Profiles").select("*").eq("id", profile_id).single().execute()

#Update profile
def update_profile(profile_id, updates: dict):
    return supabase.table("Profiles").update(updates).eq("id", profile_id).execute()

#Delete profile
def delete_profile(profile_id):
    return supabase.table("Profiles").delete().eq("id", profile_id).execute() 


# =====================
# TRANSACTIONS TABLE 
# =====================


#Create transaction
def create_transaction(user_id, category, type, date, amount, description=None):
    return supabase.table("Transactions").insert({
        "user_id": user_id,
        "category": category,
        "type": type,
        "date": date,
        "amount": amount,
        "description": description,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

#Get transaction
def get_transactions(user_id):
    return supabase.table("Transactions").select("*").eq("user_id", user_id).order("date").execute()

#Upadate transaction
def update_transaction(transaction_id, updates: dict):
    updates["created_at"] = datetime.isoformat()
    return supabase.table("Transactions").update(updates).eq("id", transaction_id).execute()

#Delete transaction
def delete_transaction(transaction_id):
    return supabase.table("Transactions").delete().eq("id", transaction_id).execute()

# ====================
# BUDGET TABLE CRUD
# ====================


#Create budget
def create_budget(user_id, budget):
    return supabase.table("Budget").insert({
        "user_id": user_id,
        "budget": budget,
        "created_at": datetime.isoformat()
    }).execute()

#Get budget
def get_budget(user_id):
    return supabase.table("Budget").select("*").eq("user_id", user_id).order("created_at").limit(1).execute()

#Update budget
def update_budget(budget_id, new_budget):
    return supabase.table("Budget").update({
        "budget": new_budget,
        "created_at": datetime.isoformat()
    }).eq("id", budget_id).execute()

#Delete budget
def delete_budget(budget_id):
    return supabase.table("Budget").delete().eq("id", budget_id).execute()

#Get all budgets
def get_all_budgets():
    return supabase.table("Budget").select("*").order("created_at").execute()