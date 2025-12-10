"""
Scripts package for the stock data pipeline.

This package currently exposes the main pipeline entrypoint from
fetch_and_load.py so it can be imported easily in the Airflow DAG.
"""

from .fetch_and_load import main as run_pipeline  # optional convenience import

__all__ = ["run_pipeline"]
