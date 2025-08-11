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
            raise FileNotFoundError(f"CRITICAL ERROR: Data file not found at {data_path}")
        self.funds = pd.read_csv(data_path)
        print("OK: funds_sample.csv loaded successfully.")

    def _safe_to_float(self, value, default=0.0):
        try: return float(value)
        except (ValueError, TypeError): return default

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

    def get_grow_url(self, fund_name):
        safe_name = re.sub(r'\s+', '+', str(fund_name).strip())
        return f"https://www.google.com/search?q={safe_name}+mutual+fund"

    def get_recommendations(self, user_info):
        # --- NEW, SMARTER RECOMMENDATION LOGIC ---
        print("DEBUG: Generating advanced recommendations based on full profile...")
        risk = user_info.get('risk_tolerance', 'moderate')
        horizon = user_info.get('investment_horizon', '5-10')
        goal = user_info.get('investment_goal', 'wealth_creation')
        invest_amount = self._safe_to_float(user_info.get('investment_amount', 0))

        # 1. Base allocation on risk
        if risk == 'low':
            alloc = {'debt': 0.60, 'large_cap': 0.30, 'flexi_cap': 0.10}
        elif risk == 'moderate':
            alloc = {'debt': 0.20, 'large_cap': 0.40, 'flexi_cap': 0.25, 'mid_cap': 0.15}
        else: # high
            alloc = {'large_cap': 0.30, 'flexi_cap': 0.30, 'mid_cap': 0.20, 'small_cap': 0.20}

        # 2. Adjust for investment horizon
        if horizon in ['1-3', '3-5']:
            # Short horizon: increase debt, reduce small/mid caps
            alloc['debt'] = alloc.get('debt', 0) + 0.20
            alloc['small_cap'] = 0
            alloc['mid_cap'] = alloc.get('mid_cap', 0) * 0.5
        elif horizon == '10+':
            # Long horizon: can take more risk
            alloc['debt'] = max(0, alloc.get('debt', 0) - 0.10)
            
        # 3. Adjust for specific goals
        if goal == 'tax_saving':
            # Ensure ELSS (tax_saving) funds are included
            alloc['tax_saving'] = alloc.get('tax_saving', 0) + 0.15

        # 4. Normalize percentages to add up to 100%
        total_pct = sum(alloc.values())
        alloc = {k: v / total_pct for k, v in alloc.items() if v > 0}

        # 5. Create final allocation dictionary with amounts
        final_allocations = {
            k: {'percentage': round(v * 100), 'amount': round(invest_amount * v)}
            for k, v in alloc.items()
        }

        # 6. Get top funds for each allocated category
        recommendations = {}
        for cat in final_allocations.keys():
            recommendations[cat] = self.get_top_funds(cat, top_n=2)
            
        return {
            'recommendations': recommendations,
            'allocations': final_allocations,
            'risk_profile': risk
        }
