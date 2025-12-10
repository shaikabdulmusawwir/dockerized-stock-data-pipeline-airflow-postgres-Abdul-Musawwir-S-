# Dockerized Stock Data Pipeline (Airflow + PostgreSQL)

This project implements a Dockerized data pipeline that automatically fetches stock market data from a public API, parses it, and stores it in a PostgreSQL database, orchestrated by Apache Airflow. It is designed to satisfy an internship technical assignment requiring a robust, containerized ETL pipeline.  

## 🎯 Objectives

- Fetch JSON stock data from a free API (e.g., Alpha Vantage) on a schedule (daily or hourly).  
- Parse the API response and extract relevant fields (symbol, price, volume, timestamp, etc.).  
- Load the data into a PostgreSQL table using a Python script.  
- Orchestrate the pipeline with an Airflow DAG running in Docker.  
- Use environment variables for API keys and database credentials.  
- Start the whole system with a single `docker compose up` command.  

## 🧱 Architecture

- **Apache Airflow (Docker container)**  
  - Hosts the scheduler and webserver.  
  - Contains the DAG `stock_pipeline_dag` which triggers the Python pipeline.  

- **PostgreSQL (Docker container)**  
  - Stores the `stock_prices` table created via `init_db.sql`.  

- **Python Scripts (mounted into Airflow container)**  
  - `scripts/fetch_and_load.py`  
    - Uses `requests` to call the stock API.  
    - Parses JSON and inserts rows into PostgreSQL using `psycopg2-binary`.  

All services run as containers managed by Docker Compose.  

## 📁 Project Structure

.
├── docker-compose.yml
├── init_db.sql
├── requirements.txt
├── .env
├── dags/
│ ├── init.py
│ └── stock_pipeline_dag.py
└── scripts/
├── init.py
└── fetch_and_load.py
