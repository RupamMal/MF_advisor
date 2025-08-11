# mutual_fund_analyzer.py
import os
import pandas as pd
import numpy as np
import re
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "funds_sample.csv"

class MutualFundAnalyzer:
    def __init__(self, data_path=DATA_PATH):
        if not data_path.exists()  or os.path.getsize(data_path) == 0:
            data_path.parent.mkdir(parents=True, exist_ok=True)
            sample_data = pd.DataFrame([
                {
                    "id": "F001",
                    "name": "Sample Large Cap Fund",
                    "category": "large_cap",
                    "nav": 120.5,
                    "aum_cr": 5000,
                    "expense_ratio": 0.8,
                    "returns_1y": 12.4,
                    "returns_3y": 11.0,
                    "returns_5y": 10.2,
                    "alpha": 1.2,
                    "beta": 0.9,
                    "sharpe": 0.8,
                    "sortino": 1.1,
                    "esg_score": 6.5,
                    "min_investment": 500
                },
                {
                    "id": "F002",
                    "name": "Sample Mid Cap Fund",
                    "category": "mid_cap",
                    "nav": 95.3,
                    "aum_cr": 3000,
                    "expense_ratio": 1.2,
                    "returns_1y": 15.4,
                    "returns_3y": 13.1,
                    "returns_5y": 12.8,
                    "alpha": 1.5,
                    "beta": 1.1,
                    "sharpe": 0.75,
                    "sortino": 1.05,
                    "esg_score": 6.0,
                    "min_investment": 1000
                }
            ])
            sample_data.to_csv(data_path, index=False)

        self.funds = pd.read_csv(data_path)

    def get_grow_url(self, fund_name):
        safe_name = re.sub(r'\s+', '+', fund_name.strip())
        return f"https://www.google.com/search?q={safe_name}+mutual+fund"

    def score_fund(self, row):
        return (
            row.get('returns_5y', 0) * 0.4 +
            row.get('sharpe', 0) * 10 * 0.25 +
            (10 - row.get('expense_ratio', 0)) * 0.15 +
            row.get('alpha', 0) * 0.2
        )

    def get_top_funds(self, category='large_cap', top_n=5):
        df = self.funds[self.funds['category'] == category].copy()
        if df.empty:
            df = self.funds.copy()
        df['score'] = df.apply(self.score_fund, axis=1)
        df = df.sort_values('score', ascending=False).head(top_n)
        return df.to_dict(orient='records')

    def get_fund_details(self, fund_id):
        row = self.funds[self.funds['id'] == fund_id]
        if row.empty:
            raise ValueError("Fund not found")
        return row.iloc[0].to_dict()

    def get_recommendations(self, user_info):
        risk = user_info.get('risk_tolerance', 'moderate')
        invest = user_info.get('investment_amount', 
                 user_info.get('lumpsum_investment', 0) + 
                 user_info.get('sip_investment', 0))

        if risk == 'low':
            alloc = {
                'debt': {'percentage': 60, 'amount': invest * 0.6},
                'large_cap': {'percentage': 20, 'amount': invest * 0.2},
                'mid_small': {'percentage': 10, 'amount': invest * 0.1},
                'tax_saving': {'percentage': 10, 'amount': invest * 0.1}
            }
        elif risk == 'high':
            alloc = {
                'large_cap': {'percentage': 40, 'amount': invest * 0.4},
                'mid_small': {'percentage': 30, 'amount': invest * 0.3},
                'flexi_cap': {'percentage': 20, 'amount': invest * 0.2},
                'tax_saving': {'percentage': 10, 'amount': invest * 0.1}
            }
        else:
            alloc = {
                'large_cap': {'percentage': 35, 'amount': invest * 0.35},
                'mid_small': {'percentage': 25, 'amount': invest * 0.25},
                'debt': {'percentage': 20, 'amount': invest * 0.2},
                'tax_saving': {'percentage': 20, 'amount': invest * 0.2}
            }

        recommendations = {}
        for cat in alloc.keys():
            cat_key = cat if cat in self.funds['category'].unique() else 'large_cap'
            recommendations[cat] = self.get_top_funds(cat_key, top_n=3)

        return {
            'recommendations': recommendations,
            'allocations': alloc
        }
