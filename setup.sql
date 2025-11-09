-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Create transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('BUY', 'SELL')),
    units INTEGER NOT NULL CHECK (units > 0),
    price NUMERIC(10, 2) NOT NULL,
    date DATE NOT NULL
);

-- Create mock prices table
CREATE TABLE prices (
    symbol VARCHAR(20) PRIMARY KEY,
    current_price NUMERIC(10, 2) NOT NULL
);

-- Sample mock prices
INSERT INTO prices (symbol, current_price) VALUES
('TCS', 3400),
('INFY', 1500),
('RELIANCE', 2600);
