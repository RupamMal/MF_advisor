from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

from mutual_fund_analyzer import MutualFundAnalyzer
from llm_recommender import LLMRecommender

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'a-strong-default-secret-key')

print("--- Flask App Initializing ---")
if not os.getenv('GEMINI_API_KEY'):
    print("CRITICAL STARTUP WARNING: GEMINI_API_KEY IS NOT SET.")
else:
    print("OK: GEMINI_API_KEY found.")

try:
    analyzer = MutualFundAnalyzer()
    llm_recommender = LLMRecommender()
    print("OK: Analyzer and LLMRecommender initialized.")
except Exception as e:
    print(f"CRITICAL STARTUP ERROR: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    print("\n--- Received /analyze request ---")
    try:
        data = request.get_json()
        
        # --- Updated to receive ALL fields from the detailed form ---
        user_info = {
            'name': data.get('name', 'User'),
            'age': data.get('age', 30),
            'annual_income': data.get('annual_income', 500000),
            'investment_amount': data.get('investment_amount', 50000),
            'risk_tolerance': data.get('risk_tolerance', 'moderate'),
            'investment_goal': data.get('investment_goal', 'wealth_creation'),
            'investment_horizon': data.get('investment_horizon', '5-10'),
            'monthly_sip': data.get('monthly_sip', 0),
            'existing_investments': data.get('existing_investments', 0),
            'tax_bracket': data.get('tax_bracket', 30),
            'emergency_fund': data.get('emergency_fund', 'yes'),
            'fund_type_preference': data.get('fund_type_preference', 'direct'),
            'esg_preference': data.get('esg_preference', 'no_preference'),
            'dividend_preference': data.get('dividend_preference', 'growth'),
        }
        print(f"DEBUG: Processing user_info: {user_info}")
        
        # --- Using the LIVE AI call ---
        print("DEBUG: Getting basic recommendations...")
        recommendations = analyzer.get_recommendations(user_info)
        
        print("DEBUG: Getting AI analysis...")
        llm_analysis = llm_recommender.generate_recommendations(user_info, recommendations)
        
        for category, funds in recommendations.get('recommendations', {}).items():
            for fund in funds:
                fund['grow_url'] = analyzer.get_grow_url(fund.get('name', ''))
        
        response_data = {
            'success': True,
            'recommendations': recommendations,
            'llm_analysis': llm_analysis,
            'user_info': user_info
        }
        
        print("--- /analyze request completed successfully. ---")
        return jsonify(response_data)
        
    except Exception as e:
        error_traceback_string = traceback.format_exc()
        print(f"--- CRASH IN /analyze ---\n{error_traceback_string}\n--------------------")
        return jsonify({
            'success': False,
            'error': 'A fatal server-side error occurred.',
            'debug_traceback': error_traceback_string 
        }), 500

@app.route('/top-funds', methods=['POST'])
def get_top_funds():
    print("\n--- Received /top-funds request ---")
    try:
        data = request.get_json()
        category = data.get('category', 'large_cap')
        top_funds = analyzer.get_top_funds(category)
        for fund in top_funds:
            fund['grow_url'] = analyzer.get_grow_url(fund.get('name', ''))
        return jsonify({'success': True, 'funds': top_funds})
    except Exception as e:
        error_traceback_string = traceback.format_exc()
        print(f"--- CRASH IN /top-funds ---\n{error_traceback_string}\n-----------------------")
        return jsonify({'success': False, 'error': str(e)}), 500
