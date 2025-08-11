from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from mutual_fund_analyzer import MutualFundAnalyzer
from llm_recommender import LLMRecommender
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# --- DEBUGGING: Check if keys are loaded at startup ---
print("Flask App Starting...")
if os.getenv('GEMINI_API_KEY'):
    print("GEMINI_API_KEY found.")
else:
    print("CRITICAL: GEMINI_API_KEY IS NOT FOUND.")
# ---

# Initialize components
analyzer = MutualFundAnalyzer()
llm_recommender = LLMRecommender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    print("\n--- Received new request for /analyze ---") # DEBUGGING
    try:
        data = request.get_json()
        print(f"DEBUG: Received user data: {json.dumps(data, indent=2)}") # DEBUGGING
        
        user_info = {
            'name': data.get('name'),
            'age': int(data.get('age')),
            'annual_income': float(data.get('annual_income')),
            'investment_amount': float(data.get('investment_amount')),
            'risk_tolerance': data.get('risk_tolerance', 'moderate'),
            'investment_goal': data.get('investment_goal', 'wealth_creation'),
            'investment_horizon': data.get('investment_horizon', '5-10 years'),
            'monthly_sip': float(data.get('monthly_sip', 0)),
            'existing_investments': float(data.get('existing_investments', 0)),
            'tax_bracket': int(data.get('tax_bracket', 20)),
            'emergency_fund': data.get('emergency_fund', 'yes'),
            'fund_type_preference': data.get('fund_type_preference', 'direct'),
            'esg_preference': data.get('esg_preference', 'no_preference'),
            'dividend_preference': data.get('dividend_preference', 'growth'),
            'lumpsum_investment': float(data.get('lumpsum_investment', 0)),
            'sip_investment': float(data.get('sip_investment', 0))
        }
        
        print("DEBUG: Step 1 - Calling MutualFundAnalyzer...") # DEBUGGING
        recommendations = analyzer.get_recommendations(user_info)
        print("DEBUG: Step 1 - MutualFundAnalyzer finished successfully.") # DEBUGGING
        
        for category, funds in recommendations['recommendations'].items():
            for fund in funds:
                fund['grow_url'] = analyzer.get_grow_url(fund['name'])
        
        print("DEBUG: Step 2 - Calling LLMRecommender...") # DEBUGGING
        llm_analysis = llm_recommender.generate_recommendations(user_info, recommendations)
        print("DEBUG: Step 2 - LLMRecommender finished successfully.") # DEBUGGING
        
        print("DEBUG: Step 3 - Preparing final JSON response...") # DEBUGGING
        response_data = {
            'success': True,
            'recommendations': recommendations,
            'llm_analysis': llm_analysis,
            'user_info': user_info
        }
        
        print("--- /analyze request completed successfully. Sending response. ---") # DEBUGGING
        return jsonify(response_data)
        
    except Exception as e:
        # This will catch any error within this function and log it clearly.
        print(f"!!!!!!!!!!!!!! CRITICAL ERROR IN /analyze ROUTE !!!!!!!!!!!!!!")
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR DETAILS: {e}")
        import traceback
        traceback.print_exc()
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# The other routes remain the same...
@app.route('/fund-details/<fund_id>')
def fund_details(fund_id):
    # ...
    return jsonify({})

@app.route('/top-funds', methods=['POST'])
def get_top_funds():
    print("\n--- Received request for /top-funds ---") # LOGGING
    try:
        data = request.get_json()
        category = data.get('category', 'large_cap')
        print(f"DEBUG: Category requested: {category}") # LOGGING
        
        top_funds = analyzer.get_top_funds(category)
        
        # LOGGING: Check what the analyzer returned
        print(f"DEBUG: Found {len(top_funds)} funds for category '{category}'.")

        return jsonify({
            'success': True,
            'funds': top_funds
        })
        
    except Exception as e:
        # LOGGING: This will now clearly log the exact error to Vercel
        print(f"!!!!!!!!!!!!!! CRITICAL ERROR IN /top-funds ROUTE !!!!!!!!!!!!!!")
        import traceback
        traceback.print_exc() # This prints the full error traceback
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        # Return a clear error message to the frontend
        return jsonify({
            'success': False,
            'error': f"A server error occurred: {str(e)}"
        }), 500
