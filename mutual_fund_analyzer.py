import pandas as pd
import numpy as np
import re
from pathlib import Path
import os

DATA_PATH = Path(__file__).parent / "data" / "funds_sample.csv"

class MutualFundAnalyzer:
    def __init__(self, data_path=DATA_PATH):
        print("DEBUG: Initializing MutualFundAnalyzer...")
        if not data_path.is_file():
            raise FileNotFoundError(f"CRITICAL ERROR: The data file was not found at the expected path: {data_path}")
        
        self.funds = pd.read_csv(data_path)
        print("OK: funds_sample.csv loaded successfully.")

    def _safe_to_float(self, value, default=0.0):
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def score_fund(self, row):
        sip_5yr_return = self._safe_to_float(row.get('sip_5yr_return'))
        sharpe_ratio = self._safe_to_float(row.get('sharpe_ratio'))
        expense_ratio = self._safe_to_float(row.get('expense_ratio'), 2.0)
        alpha = self._safe_to_float(row.get('alpha'))
        returns_score = sip_5yr_return * 0.4
        risk_adjusted_score = sharpe_ratio * 10 * 0.25
        expense_score = (2 - expense_ratio) * 0.15
        alpha_score = alpha * 0.2
        return returns_score + risk_adjusted_score + expense_score + alpha_score

    def get_top_funds(self, category='large_cap', top_n=5):
        df = self.funds.copy()
        if category and category in df['category'].unique():
            df = df[df['category'] == category]
        if df.empty: return []
        df['score'] = df.apply(self.score_fund, axis=1)
        return df.sort_values('score', ascending=False).head(top_n).to_dict(orient='records')

    def get_recommendations(self, user_info):
        risk = user_info.get('risk_tolerance', 'moderate')
        invest = self._safe_to_float(user_info.get('investment_amount', 0))
        alloc = {}
        if risk == 'low':
            alloc = {'debt': 0.6, 'large_cap': 0.4}
        else: # moderate or high
            alloc = {'large_cap': 0.6, 'flexi_cap': 0.4}
        
        final_allocations = {k: {'percentage': v * 100, 'amount': invest * v} for k, v in alloc.items()}
        
        recommendations = {}
        for cat in alloc.keys():
            recommendations[cat] = self.get_top_funds(cat, top_n=2)
            
        return {'recommendations': recommendations, 'allocations': final_allocations, 'risk_profile': risk}

    def get_grow_url(self, fund_name):
        safe_name = re.sub(r'\s+', '+', str(fund_name).strip())
        return f"https://www.google.com/search?q={safe_name}+mutual+fund"
