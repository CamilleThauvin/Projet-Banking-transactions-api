from fastapi import FastAPI
import os
from banking_api.services import transactions_service

app = FastAPI(title="Banking Transactions API")

@app.get("/api/system/health", tags=["System"])
def get_health():
    dataset_exists = os.path.exists("data/transactions_data.csv")
    return {"status": "ok", "dataset_loaded": dataset_exists}

@app.get("/api/transactions", tags=["Transactions"])
def read_transactions(page: int = 1, limit: int = 10):
    return transactions_service.get_paginated_transactions(page, limit)

@app.get("/api/transactions/stats", tags=["Statistiques"])
def read_stats():
    return transactions_service.get_global_stats()