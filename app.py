from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import traceback

# --- It's critical to import your other files AFTER the dotenv load ---
load_dotenv()

from mutual_fund_analyzer import MutualFundAnalyzer
from llm_recommender import LLMRecommender

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'a-strong-default-secret-key')

# --- Startup Check ---
print("--- Flask App Initializing ---")
if not os.getenv('GEMINI_API_KEY'):
    print("CRITICAL STARTUP WARNING: GEMINI_API_KEY IS NOT SET IN THIS ENVIRONMENT.")
else:
    print("OK: GEMINI_API_KEY environment variable was found.")
# ---

try:
    analyzer = MutualFundAnalyzer()
    llm_recommender = LLMRecommender()
    print("OK: Analyzer and LLMRecommender initialized successfully.")
except Exception as e:
    print(f"CRITICAL STARTUP ERROR: Failed to initialize components. Error: {e}")
    traceback.print_exc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    print("\n--- Received new request for /analyze ---")
    try:
        data = request.get_json()
        user_info = data # Use the whole data object
        
        print("DEBUG: Step 1 - Calling MutualFundAnalyzer...")
        recommendations = analyzer.get_recommendations(user_info)
        print("DEBUG: Step 1 - MutualFundAnalyzer finished successfully.")
        
        for category, funds in recommendations.get('recommendations', {}).items():
            for fund in funds:
                fund['grow_url'] = analyzer.get_grow_url(fund['name'])
        
        # --- DIAGNOSTIC STEP: THE REAL AI CALL IS DISABLED ---
        print("DEBUG: Step 2 - SKIPPING REAL LLM CALL FOR DIAGNOSTICS.")
        # llm_analysis = llm_recommender.generate_recommendations(user_info, recommendations)
        
        # Using placeholder data to prevent external API crash
        llm_analysis = {
            "summary": "This is a placeholder summary. If you see this, the application logic is working.",
            "key_insights": ["The external AI call is temporarily disabled for debugging."],
            "suggested_allocations": recommendations.get("allocations", {}),
            "sections": {"investment_thesis": "Placeholder thesis."}
        }
        print("DEBUG: Step 2 - Using dummy LLM data.")
        
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
        print("--- A CRASH OCCURRED IN /analyze ---")
        print(error_traceback_string)
        print("------------------------------------")
        return jsonify({
            'success': False,
            'error': 'A fatal server-side error occurred.',
            'debug_traceback': error_traceback_string 
        }), 500

@app.route('/top-funds', methods=['POST'])
def get_top_funds():
    print("\n--- Received request for /top-funds ---")
    try:
        data = request.get_json()
        category = data.get('category', 'large_cap')
        print(f"DEBUG: Category requested: {category}")
        top_funds = analyzer.get_top_funds(category)
        print(f"DEBUG: Found {len(top_funds)} funds for category '{category}'.")
        return jsonify({'success': True, 'funds': top_funds})
    except Exception as e:
        error_traceback_string = traceback.format_exc()
        print("--- A CRASH OCCURRED IN /top-funds ---")
        print(error_traceback_string)
        print("--------------------------------------")
        return jsonify({'success': False, 'error': str(e)}), 500
