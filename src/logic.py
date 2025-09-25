# src/logic.py
from src.db import (
    create_profile,
    get_all_profiles,
    get_profile,
    update_profile,
    delete_profile,
    create_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
    create_budget,
    get_budget,
    update_budget,
    delete_budget
)

# =========================
# PROFILE SERVICE
# =========================
class ProfileService:
    """
    Service to manage user profiles. Acts as a bridge between API/frontend and database functions.
    """

    def add_profile(self, username):
        """Add a new profile."""
        if not username:
            return {"Success": False, "Message": "Username is required"}

        try:
            result = create_profile(username)
            if result.data:
                return {"Success": True, "Message": "Profile added successfully"}
            else:
                return {"Success": False, "Message": "Failed to add profile"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def list_profiles(self):
        """Get all profiles."""
        try:
            result = get_all_profiles()
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def get_profile(self, profile_id):
        """Get a single profile by ID."""
        try:
            result = get_profile(profile_id)
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def update_profile(self, profile_id, username):
        """Update profile username."""
        try:
            result = update_profile(profile_id, {"username": username})
            return {"Success": True, "Message": "Profile updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def delete_profile(self, profile_id):
        """Delete profile by ID."""
        try:
            result = delete_profile(profile_id)
            return {"Success": True, "Message": "Profile deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}


# =========================
# TRANSACTION SERVICE
# =========================
class TransactionService:
    """Service to manage user transactions."""

    def add_transaction(self, user_id, category, type_, date, amount, description=None):
        """Add a new transaction."""
        try:
            result = create_transaction(user_id, category, type_, date, amount, description)
            return {"Success": True, "Message": "Transaction added successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def list_transactions(self, user_id):
        """Get all transactions for a user."""
        try:
            result = get_transactions(user_id)
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def update_transaction(self, transaction_id, updates: dict):
        """Update a transaction."""
        try:
            result = update_transaction(transaction_id, updates)
            return {"Success": True, "Message": "Transaction updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def delete_transaction(self, transaction_id):
        """Delete a transaction."""
        try:
            result = delete_transaction(transaction_id)
            return {"Success": True, "Message": "Transaction deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}


# =========================
# BUDGET SERVICE
# =========================
class BudgetService:
    """Service to manage user budgets."""

    def set_budget(self, user_id, budget):
        """Set a new budget."""
        try:
            result = create_budget(user_id, budget)
            return {"Success": True, "Message": "Budget set successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def get_budget(self, user_id):
        """Get the latest budget for a user."""
        try:
            result = get_budget(user_id)
            return {"Success": True, "Data": result.data}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def update_budget(self, budget_id, new_budget):
        """Update an existing budget."""
        try:
            result = update_budget(budget_id, new_budget)
            return {"Success": True, "Message": "Budget updated successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}

    def delete_budget(self, budget_id):
        """Delete a budget."""
        try:
            result = delete_budget(budget_id)
            return {"Success": True, "Message": "Budget deleted successfully"}
        except Exception as e:
            return {"Success": False, "Message": f"Error: {str(e)}"}
