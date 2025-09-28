from src.db import (
    create_profile, get_all_profiles, get_profile, update_profile, delete_profile,
    create_transaction, get_transactions, update_transaction, delete_transaction,
    create_budget, get_budget, update_budget, delete_budget,
    get_profile_by_username, get_profile_by_email
)
import bcrypt

# =========================
# PROFILE SERVICE
# =========================
class ProfileService:

    def add_profile(self, username, email=None, password=None):
        if not username or not password:
            return {"Success": False, "Message": "Username and password required"}
        try:
            # Check if username/email exists
            if email:
                existing = get_profile_by_email(email).data
            else:
                existing = get_profile_by_username(username).data

            if existing:
                return {"Success": False, "Message": "User already exists"}
            
            result = create_profile(username, email, password)
            if result.data:
                return {"Success": True, "Message": "Profile added successfully"}
            else:
                return {"Success": False, "Message": "Failed to add profile"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def list_profiles(self):
        try:
            result = get_all_profiles()
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def get_profile(self, profile_id):
        try:
            result = get_profile(profile_id)
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def update_profile(self, profile_id, username):
        try:
            result = update_profile(profile_id, {"username": username})
            return {"Success": True, "Message": "Profile updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def delete_profile(self, profile_id):
        try:
            result = delete_profile(profile_id)
            return {"Success": True, "Message": "Profile deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def login(self, username_or_email, password):
        try:
            result = get_profile_by_username(username_or_email).data
            if not result:
                result = get_profile_by_email(username_or_email).data
            if not result:
                return {"Success": False, "Message": "User not found. Please register first."}
            user = result[0]
            if bcrypt.checkpw(password.encode(), user["password"].encode()):
                return {"Success": True, "Message": "Login successful", "Data": user}
            else:
                return {"Success": False, "Message": "Incorrect password"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

# =========================
# TRANSACTION SERVICE
# =========================
class TransactionService:
    def add_transaction(self, user_id, category, type_, date, amount, description=None):
        try:
            result = create_transaction(user_id, category, type_, date, amount, description)
            return {"Success": True, "Message": "Transaction added successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def list_transactions(self, user_id):
        try:
            result = get_transactions(user_id)
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def update_transaction(self, transaction_id, updates: dict):
        try:
            if "type_" in updates:
                updates["type"] = updates.pop("type_")  # map for DB
            result = update_transaction(transaction_id, updates)
            return {"Success": True, "Message": "Transaction updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}


    def delete_transaction(self, transaction_id):
        try:
            result = delete_transaction(transaction_id)
            return {"Success": True, "Message": "Transaction deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

# =========================
# BUDGET SERVICE
# =========================
class BudgetService:
    def set_budget(self, user_id, budget):
        try:
            result = create_budget(user_id, budget)
            return {"Success": True, "Message": "Budget set successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def get_budget(self, user_id):
        try:
            result = get_budget(user_id)
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def update_budget(self, budget_id, new_budget):
        try:
            result = update_budget(budget_id, new_budget)
            return {"Success": True, "Message": "Budget updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def delete_budget(self, budget_id):
        try:
            result = delete_budget(budget_id)
            return {"Success": True, "Message": "Budget deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}
