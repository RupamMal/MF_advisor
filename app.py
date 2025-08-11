from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from mutual_fund_analyzer import MutualFundAnalyzer
from llm_recommender import LLMRecommender
import json
import traceback

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
# It's a good practice to have a secret key for web applications
app.secret_key = os.getenv('SECRET_KEY', 'a-strong-default-secret-key')

# --- Startup Check ---
# This print statement will appear in the Vercel deployment logs at the very beginning.
print("Flask App Initializing...")
if not os.getenv('GEMINI_API_KEY'):
    print("CRITICAL WARNING: The GEMINI_API_KEY environment variable is NOT set.")
else:
    print("Successfully found GEMINI_API_KEY environment variable.")
# ---

# Initialize your application components
try:
    analyzer = MutualFundAnalyzer()
    llm_recommender = LLMRecommender()
    print("Analyzer and LLMRecommender initialized successfully.")
except Exception as e:
    print(f"CRITICAL STARTUP ERROR: Failed to initialize components. Error: {e}")
    traceback.print_exc()

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    The main endpoint that receives user data, gets recommendations,
    and returns a full analysis.
    """
    print("\n--- Received new request for /analyze ---")
    try:
        # Get user data from the frontend
        data = request.get_json()
        
        # Structure the user info
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
        
        # Step 1: Get basic recommendations from the analyzer
        print("DEBUG: Step 1 - Calling MutualFundAnalyzer...")
        recommendations = analyzer.get_recommendations(user_info)
        print("DEBUG: Step 1 - MutualFundAnalyzer finished successfully.")
        
        # Add a direct link for each recommended fund
        for category, funds in recommendations.get('recommendations', {}).items():
            for fund in funds:
                fund['grow_url'] = analyzer.get_grow_url(fund['name'])
        
        # Step 2: Get the AI-powered analysis
        print("DEBUG: Step 2 - Calling LLMRecommender...")
        llm_analysis = llm_recommender.generate_recommendations(user_info, recommendations)
        print("DEBUG: Step 2 - LLMRecommender finished successfully.")
        
        # Prepare the final successful response
        response_data = {
            'success': True,
            'recommendations': recommendations,
            'llm_analysis': llm_analysis,
            'user_info': user_info
        }
        
        print("--- /analyze request completed successfully. ---")
        return jsonify(response_data)
        
    except Exception as e:
        # --- THIS IS THE FAILSAFE ERROR REPORTING BLOCK ---
        # If any part of the 'try' block fails, this code will run.
        
        # Get the full error traceback as a text string
        error_traceback_string = traceback.format_exc()
        
        # Print the full error to the Vercel logs for our own debugging
        print("--- A CRASH OCCURRED IN /analyze ---")
        print(error_traceback_string)
        print("------------------------------------")

        # Return a response that includes the detailed error message.
        # The frontend is now designed to display this.
        return jsonify({
            'success': False,
            'error': 'A fatal server-side error occurred while processing your request.',
            'debug_traceback': error_traceback_string 
        }), 500

@app.route('/top-funds', methods=['POST'])
def get_top_funds():
    """Endpoint to get the top 5 funds for a specific category."""
    print("\n--- Received request for /top-funds ---")
    try:
        data = request.get_json()
        category = data.get('category', 'large_cap')
        print(f"DEBUG: Category requested: {category}")
        
        top_funds = analyzer.get_top_funds(category)
        
        print(f"DEBUG: Found {len(top_funds)} funds for category '{category}'.")
        return jsonify({
            'success': True,
            'funds': top_funds
        })
        
    except Exception as e:
        # Also add the failsafe block to this endpoint
        error_traceback_string = traceback.format_exc()
        print("--- A CRASH OCCURRED IN /top-funds ---")
        print(error_traceback_string)
        print("--------------------------------------")
        return jsonify({
            'success': False,
            'error': 'A fatal server-side error occurred while fetching top funds.',
            'debug_traceback': error_traceback_string
        }), 500
