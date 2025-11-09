# WealthWise-Portfolio-Tracker  
A FastAPI-based backend that helps users manage and track their stock portfolios.
It allows users to add transactions, view holdings, calculate profit/loss, and see current portfolio summaries using mock market prices.  

##  Features

-  **Add New Users**  
  Easily create and manage user accounts.

-  **Record BUY and SELL Transactions**  
  Supports both buy and sell types with validation.

-  **Fetch Portfolio Summaries**  
  Displays current holdings, total portfolio value, and returns.

-  **View Transaction History**  
  Lists all user transactions with date, price, and quantity details.

-  **Automatic Calculations**  
  -  **Weighted Average Cost** – dynamically computed per stock.  
  -  **Current Portfolio Value** – based on mock market prices.  
  -  **Unrealized Profit/Loss** – total gain or loss per holding.


## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Maithiliii/WealthWise-Portfolio-Tracker.git
cd WealthWise-Portfolio-Tracker
```   
### 2. Create and Activate a Virtual Environment
```bash  
python -m venv venv  
venv\Scripts\activate   # on Windows  
# OR  
source venv/bin/activate  # on macOS/Linux  
```
### 3. Install Dependencies
```bash  
pip install -r requirements.txt
```
### 4. Set Up Your Environment Variables
Create a .env file in the project root:
```bash  
DB_HOST=localhost
DB_NAME=wealthwise
DB_USER=postgres
DB_PASSWORD=postgre
DB_PORT=5432
```
### 5.Database Setup
In PostgreSQL, create a new database:
```bash
CREATE DATABASE wealthwise;
```
Then create the tables:
In PostgreSQL, create a new database:
```bash
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    symbol VARCHAR(20),
    type VARCHAR(10),
    units INT,
    price FLOAT,
    date DATE
);
```

### Running the App  
Start the FastAPI server:  
```bash
uvicorn main:app --reload
```
Access the API docs:
```bash
http://127.0.0.1:8000/docs
```

### Example API Usage
#### Add User

POST /user
```bash  
{
  "name": "Maithili",
  "email": "maithili@example.com"
}
```
#### Add Transaction

POST /transaction
```bash  
{
  "user_id": 1,
  "symbol": "TCS",
  "type": "BUY",
  "units": 5,
  "price": 3200,
  "date": "2025-05-10"
}
```
#### Get Portfolio Summary

GET /portfolio-summary?user_id=1
```bash  
{
  "user_id": 1,
  "holdings": [
    {
      "symbol": "TCS",
      "units": 5,
      "avg_cost": 3200,
      "current_price": 3400,
      "unrealized_pl": 1000
    }
  ],
  "total_value": 17000,
  "total_gain": 1000
}
```

#### Get Transaction History

GET /transactions?user_id=1
```bash  
{
  "user_id": 1,
  "transactions": [
    {
      "symbol": "TCS",
      "type": "BUY",
      "units": 5,
      "price": 3200,
      "date": "2025-05-10"
    }
  ]
}
```
