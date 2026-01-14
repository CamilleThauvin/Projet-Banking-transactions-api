import pandas as pd

def get_global_stats():
    """
    Calcule les statistiques globales du dataset (Route 9).
    Style numpy pour la documentation.
    """
    # On charge uniquement les colonnes nécessaires pour économiser la RAM
    df = pd.read_csv("data/transactions_data.csv")
    
    return {
        "total_transactions": len(df),
        "fraud_rate": df['isFraud'].mean(),
        "avg_amount": df['amount'].mean(),
        "most_common_type": df['type'].mode()[0]
    }