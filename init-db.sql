CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price NUMERIC(18,6),
    volume BIGINT,
    ts TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
