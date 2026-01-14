import csv
import os
from fastapi import HTTPException

def get_paginated_transactions(page: int, limit: int):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

    transactions = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            start_index = (page - 1) * limit
            for i, row in enumerate(reader):
                if i < start_index:
                    continue
                if len(transactions) < limit:
                    transactions.append(row)
                else:
                    break
        return {"status": "success", "data": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_global_stats():
    """
    Route 9 : Compte les lignes sans saturer la RAM.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "transactions_data.csv")

    try:
        count = 0
        with open(csv_path, 'rb') as f:
            for _ in f:
                count += 1
        return {
            "total_transactions": count - 1, # -1 pour le header
            "file_size": f"{round(os.path.getsize(csv_path) / (1024**3), 2)} Go"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))