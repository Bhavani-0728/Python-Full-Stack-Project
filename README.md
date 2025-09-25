# 💰 Full-Stack Expense Tracker

A user-friendly full-stack web application to manage personal finances. Users can track income and expenses, categorize transactions, and visualize spending trends using charts. This project demonstrates a complete full-stack application using Python, FastAPI, Supabase, and Streamlit.

## 🌟 Features

- **💵 Transaction Management**: Add, view, update, and delete income and expenses.
- **📊 Dashboard & Charts**: Visualize monthly spending and category-wise expenses.
- **🔖 Categories**: Organize transactions by category (Food, Travel, Bills, etc.).
- **🗓️ Date Tracking**: Record transaction dates for accurate monthly reports.
- **🔐 User Authentication**: Secure signup and login using Supabase Auth.
- **📈 Expense Reports**: Analyze spending trends over time.
- **💻 Responsive Design**: Clean, modern interface for desktop and mobile.

## Project Structure

EXPENSETRACKER/                 
│
|--- src/                           #core application logic
│     |__logic.py                   #Business logic and task
operations
|     |__db.py                      #Database operations 
|
|--- api/                           #Backend API
|     |__main.py                    #FastAPI endpoints
|
|--- frontend/                      # Frontend application
│     |__app.py                     # Streamlit web interface
|
|____requirements.txt               # Python Dependencies
|
|____README.md                      # Project documentation
|
|____.env                           # Python variables


## Quick Start

### Prerequisites

- Python 3.8 or higher
- A supabase account
- Git(Push, Cloning)

### 1. Clone or Download the Project

### Option 1: Clone with git
git clone <repository-url> 

### Option 2: Download and extract the ZIP file

### 2. Install Dependencies

### Install all required Python packages
pip install -r requirements.txt

### 3. Set up Supabase Database

1.Create a Supabase Project:

2.Create the Tasks Table:

- Go to the SQL Editor in your Supabase dashboard
- Run this SQL command:

``` sql
CREATE TABLE Profiles (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
``` sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES profiles(id),
    category TEXT,
    type TEXT, 
    date DATE,
    amount FLOAT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
``` sql
CREATE TABLE budget (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES profiles(id),
    budget FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3.Get your credentials

### 4. Configure Environment Variables 

1. Create a `.env` file in the project root

2. Add your Supabase cedentials to `.env`:
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here

### 5. Run the Application

## FastAPI Backend

cd api
uvicorn main:app --reload --port 8000

The API will be available at `http://localhost:8000`

### Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

## How to Use

1. Add a profile.

2. Add transactions (Income or Expense) with category, date, amount, and description.

3. View all transactions in a sortable/filterable table.

4. Set a monthly budget.

5. Open Dashboard → View monthly spending trends and category-wise charts.

6. Export data as CSV/PDF (if implemented).

## 🛠Technical Details

### Technologies Used

- **Frontend**: Streamlit (Python web framework), Plotly (Visualize charts)
- **Backend**: FastAPI (Python REST API framework)
- **Database**: Supabase (PostgreSQL-based backend-as-a-service)
- **Language**: Python 3.8+

### Key Components

1. **`src/db.py`**: Database operations - Handles all CRUD operations with Supabase

2. **`src/logic.py`**: Business logic - Task validation and processing

## ⚠️Troubleshooting

## Common Issues


1. **"Module not found" error**:
    - Make sure you've installed all dependencies: `pip install -r requirements.txt`
    - Check that you're running commands from the correct directory
2. **Environment variable errors**
    - Confirm .env file exists in the project root.
    - Check variables match your Supabase project credentials.
3.  **Supabase connection errors**
    - Ensure your Supabase project is running and credentials are correct.
    - If on free tier, wait if API requests are rate-limited.
4.  **Streamlit not launching in browser**
    - Try http://localhost:8501 manually.
    - Check if another process is already using that port.
5. **Supabase Table Not Found**
    - Ensure table names are lowercase (profiles, transactions, budget).
6.  **JSONDecodeError in Streamlit**
    - Happens when the API returns invalid JSON. Ensure backend is running and endpoints match frontend requests.


## 🚀Future Enhacements

💳 Multi-Currency Support: Track expenses in different currencies with conversion rates.

📅 Recurring Transactions: Auto-add monthly/weekly recurring expenses.

📥 Import Bank Statements: Upload CSV from bank for automatic parsing.

📱 Mobile App: Deploy as PWA (Progressive Web App).

🤖 AI Insights: Suggest budget adjustments or detect unusual spending patterns.

🔔 Notifications: Email/SMS alerts when nearing budget limits.

## 📞Support 

If you encounter any issues or have questions:
    Phone Number : +91 90631997036
    Email : bhavanibhavya77@gmail.com