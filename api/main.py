# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys, os
from hashlib import sha256

# Add project root to path to import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from src.logic import ProfileService, TransactionService, BudgetService

# ------------------- App Setup -------------------
app = FastAPI(title="Expense Tracker API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Service Instances -------------------
profile_service = ProfileService()
transaction_service = TransactionService()
budget_service = BudgetService()

# ------------------- Data Models -------------------
class ProfileCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: Optional[str] = None

class ProfileLogin(BaseModel):
    username: str
    password: str

class ProfileUpdate(BaseModel):
    username: str

class TransactionCreate(BaseModel):
    user_id: int
    category: str
    type_: str
    date: str
    amount: float
    description: Optional[str] = None

class TransactionUpdate(BaseModel):
    category: Optional[str] = None
    type_: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None

class BudgetCreate(BaseModel):
    user_id: int
    budget: float

class BudgetUpdate(BaseModel):
    budget: float

# ------------------- Authentication Endpoints -------------------
@app.post("/register")
def register(profile: ProfileCreate):
    if not profile.username or not profile.email or not profile.password:
        return {"Success": False, "Message": "All fields are required"}

    # Hash password before storing
    hashed_pw = sha256(profile.password.encode()).hexdigest()
    try:
        result = profile_service.add_profile_with_credentials(profile.username, profile.email, hashed_pw)
        return result
    except Exception as e:
        return {"Success": False, "Message": f"Error: {str(e)}"}

@app.post("/login")
def login(profile: ProfileLogin):
    if not profile.username or not profile.password:
        return {"Success": False, "Message": "Username and password required"}

    hashed_pw = sha256(profile.password.encode()).hexdigest()
    try:
        user = profile_service.login(profile.username, hashed_pw)
        if user:
            return {"Success": True, "Data": user}
        else:
            return {"Success": False, "Message": "Invalid credentials or user not registered"}
    except Exception as e:
        return {"Success": False, "Message": f"Error: {str(e)}"}

# ------------------- Profile Endpoints -------------------
@app.post("/profiles")
def add_profile(profile: ProfileCreate):
    return profile_service.add_profile(profile.username)

@app.get("/profiles")
def get_profiles():
    return profile_service.list_profiles()

@app.get("/profiles/{profile_id}")
def get_profile(profile_id: int):
    return profile_service.get_profile(profile_id)

@app.put("/profiles/{profile_id}")
def update_profile(profile_id: int, profile: ProfileUpdate):
    return profile_service.update_profile(profile_id, profile.username)

@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: int):
    return profile_service.delete_profile(profile_id)

# ------------------- Transaction Endpoints -------------------
@app.post("/transactions")
def add_transaction(transaction: TransactionCreate):
    return transaction_service.add_transaction(
        transaction.user_id,
        transaction.category,
        transaction.type_,
        transaction.date,
        transaction.amount,
        transaction.description,
    )

@app.get("/transactions/{user_id}")
def get_transactions(user_id: int):
    return transaction_service.list_transactions(user_id)

@app.put("/transactions/{transaction_id}")
def update_transaction(transaction_id: int, transaction: TransactionUpdate):
    return transaction_service.update_transaction(transaction_id, transaction.dict(exclude_unset=True))

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int):
    return transaction_service.delete_transaction(transaction_id)

# ------------------- Budget Endpoints -------------------
@app.post("/budgets")
def add_budget(budget: BudgetCreate):
    return budget_service.set_budget(budget.user_id, budget.budget)

@app.get("/budgets/{user_id}")
def get_budget(user_id: int):
    return budget_service.get_budget(user_id)

@app.put("/budgets/{budget_id}")
def update_budget(budget_id: int, budget: BudgetUpdate):
    return budget_service.update_budget(budget_id, budget.budget)

@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int):
    return budget_service.delete_budget(budget_id)
