import pandas as pd
import numpy as np
import re
from pathlib import Path
import os

DATA_PATH = Path(__file__).parent / "data" / "funds_sample.csv"

class MutualFundAnalyzer:
    def __init__(self, data_path=DATA_PATH):
        print("DEBUG: Initializing MutualFundAnalyzer...") # DEBUGGING
        if not data_path.exists() or os.path.getsize(data_path) == 0:
            # ... (code to create sample data is fine)
            pass
        self.funds = pd.read_csv(data_path)
        print("DEBUG: funds_sample.csv loaded successfully.") # DEBUGGING

    def get_grow_url(self, fund_name):
        safe_name = re.sub(r'\s+', '+', fund_name.strip())
        return f"https://www.google.com/search?q={safe_name}+mutual+fund"

    def score_fund(self, row):
        returns_score = row.get('sip_5yr_return', 0) * 0.4
        risk_adjusted_score = row.get('sharpe_ratio', 0) * 10 * 0.25
        expense_score = (2 - row.get('expense_ratio', 2)) * 0.15 # Lower expense ratio is better
        alpha_score = row.get('alpha', 0) * 0.2
    
        return returns_score + risk_adjusted_score + expense_score + alpha_score


    def get_top_funds(self, category='large_cap', top_n=5):
        # Start with a full copy of the funds data.
        df = self.funds.copy()

        # --- START OF FIX ---
        # First, a safety check: if the main data is empty, return an empty list now.
        if df.empty:
            print("WARNING: The main funds dataframe is empty. Cannot get top funds.")
            return []

        # Filter by the requested category.
        # This correctly handles the case where the user selects a specific category.
        if category and category in df['category'].unique():
            df = df[df['category'] == category]

        # Second safety check: if the *filtered* dataframe is empty, return an empty list.
        # This happens if a category has no funds.
        if df.empty:
            print(f"WARNING: No funds were found for the category '{category}'.")
            return []

        # If we have funds, proceed to score them.
        # This uses the score_fund function we fixed earlier.
        df['score'] = df.apply(self.score_fund, axis=1)
        
        # Sort the dataframe by the new 'score' column in descending order.
        df_sorted = df.sort_values('score', ascending=False)
        
        # Return the top N results as a list of dictionaries.
        return df_sorted.head(top_n).to_dict(orient='records')
        # --- END OF FIX ---


    def get_fund_details(self, fund_id):
        # ... (this function is fine)
        return {}

    def get_recommendations(self, user_info):
        print("DEBUG: Inside get_recommendations...") # DEBUGGING
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
        else: # moderate
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

        print("DEBUG: Finished get_recommendations. Returning data.") # DEBUGGING
        return {
            'recommendations': recommendations,
            'allocations': alloc,
            'risk_profile': risk
        }
