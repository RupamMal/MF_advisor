from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from mutual_fund_analyzer import MutualFundAnalyzer
from llm_recommender import LLMRecommender
import json
# No need to import this twice: from flask import Flask, request, jsonify, render_template, send_from_directory

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize components
analyzer = MutualFundAnalyzer()
llm_recommender = LLMRecommender()

@app.route('/')
def index():
    # MODIFICATION: Changed 'templates\index.html' to 'index.html'.
    # Flask automatically looks for templates in a folder named "templates".
    # Using forward slashes or no path prefix is standard and works across all operating systems.
    # Ensure your 'index.html' file is inside a 'templates' folder.
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        # Extract user information with all new fields
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
        
        # Get recommendations from analyzer
        recommendations = analyzer.get_recommendations(user_info)
        
        # Add GROW URLs to each fund
        for category, funds in recommendations['recommendations'].items():
            for fund in funds:
                fund['grow_url'] = analyzer.get_grow_url(fund['name'])
        
        # Generate LLM analysis
        llm_analysis = llm_recommender.generate_recommendations(user_info, recommendations)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'llm_analysis': llm_analysis,
            'user_info': user_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/fund-details/<fund_id>')
def fund_details(fund_id):
    try:
        details = analyzer.get_fund_details(fund_id)
        return jsonify({
            'success': True,
            'details': details
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/top-funds', methods=['POST'])
def get_top_funds():
    try:
        data = request.get_json()
        category = data.get('category', 'large_cap')
        
        # Get top 5 funds for the specified category
        top_funds = analyzer.get_top_funds(category)
        
        return jsonify({
            'success': True,
            'funds': top_funds
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# NOTE: The following block is for local development.
# On a hosting platform, a Gunicorn server will run the 'app' object directly.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')