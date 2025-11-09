from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="WealthWise Portfolio Tracker")

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "wealthwise"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""), 
        port=os.getenv("DB_PORT", 5432)
    )
    return conn

class User(BaseModel):
    name: str
    email: str

class Transaction(BaseModel):
    user_id: int
    symbol: str
    type: str
    units: int
    price: float
    date: date

with open("mock_prices.json", "r") as f:
    prices = json.load(f)

@app.post("/user")
def add_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
        (user.name, user.email)
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "User created successfully", "user_id": user_id}

@app.post("/transaction")
def add_transaction(txn: Transaction):
    conn = get_db_connection()
    cur = conn.cursor()

    if txn.type not in ["BUY", "SELL"]:
        raise HTTPException(status_code=400, detail="Transaction type must be BUY or SELL")

    if txn.type == "SELL":
        cur.execute("""
            SELECT COALESCE(SUM(CASE WHEN type='BUY' THEN units ELSE -units END), 0)
            FROM transactions WHERE user_id=%s AND symbol=%s
        """, (txn.user_id, txn.symbol))
        current_units = cur.fetchone()[0]
        if txn.units > current_units:
            raise HTTPException(status_code=400, detail="Cannot sell more units than owned")

    cur.execute("""
        INSERT INTO transactions (user_id, symbol, type, units, price, date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (txn.user_id, txn.symbol, txn.type, txn.units, txn.price, txn.date))

    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Transaction added successfully"}

@app.get("/portfolio-summary")
def get_portfolio_summary(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT symbol,
               SUM(CASE WHEN type='BUY' THEN units ELSE -units END) AS total_units,
               SUM(CASE WHEN type='BUY' THEN units*price ELSE -units*price END) AS total_cost
        FROM transactions
        WHERE user_id=%s
        GROUP BY symbol
        HAVING SUM(CASE WHEN type='BUY' THEN units ELSE -units END) > 0
    """, (user_id,))

    holdings = []
    total_value = 0
    total_gain = 0

    for symbol, units, total_cost in cur.fetchall():
        avg_cost = total_cost / units
        current_price = prices.get(symbol, 0)
        value = current_price * units
        gain = (current_price - avg_cost) * units
        holdings.append({
            "symbol": symbol,
            "units": units,
            "avg_cost": round(avg_cost, 2),
            "current_price": current_price,
            "unrealized_pl": round(gain, 2)
        })
        total_value += value
        total_gain += gain

    cur.close()
    conn.close()

    return {
        "user_id": user_id,
        "holdings": holdings,
        "total_value": round(total_value, 2),
        "total_gain": round(total_gain, 2)
    }

@app.get("/transactions")
def get_transaction_history(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT symbol, type, units, price, date
        FROM transactions
        WHERE user_id=%s
        ORDER BY date DESC
    """, (user_id,))
    transactions = cur.fetchall()
    cur.close()
    conn.close()

    return {"user_id": user_id, "transactions": transactions}
