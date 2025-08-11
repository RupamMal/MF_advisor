# llm_recommender.py
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
# This check is now more important than ever
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables.")

genai.configure(api_key=API_KEY)

class LLMRecommender:
    def __init__(self, model="gemini-1.5-flash"):
        self.client = genai.GenerativeModel(model)

    def _build_prompt(self, user_info, recommendations):
        # This function remains the same
        return f"""
You are a professional mutual fund advisor.
User info: {json.dumps(user_info, indent=2)}

Recommendations: {json.dumps(recommendations, indent=2)}

Respond in valid JSON ONLY with:
{{
  "summary": "...",
  "key_insights": ["...", "...", "..."],
  "suggested_allocations": {{
     "category": {{
       "percentage": int,
       "amount": float,
       "note": "..."
     }}
  }},
  "sections": {{
    "investment_thesis": "...",
    "risk_analysis": "...",
    "implementation_steps": "...",
    "tax_notes": "..."
  }}
}}

Rules:
- Keep percentages and amounts consistent with provided data.
- Keep tone professional.
- Include disclaimer in "tax_notes".
"""

        # --- THIS IS THE NEW DIAGNOSTIC SECTION ---
        print("DEBUG: Step 2 - Temporarily SKIPPING LLMRecommender...") # DEBUGGING
        # llm_analysis = llm_recommender.generate_recommendations(user_info, recommendations) # The real call is commented out
        
        # We will use hardcoded "dummy" data instead.
        llm_analysis = {
            "summary": "This is a placeholder summary. The AI analysis is temporarily disabled for debugging.",
            "key_insights": [
                "This is a sample insight.",
                "If you see this, the main application logic is working correctly."
            ],
            "suggested_allocations": recommendations.get("allocations", {}),
            "sections": {
                "investment_thesis": "This is a placeholder investment thesis."
            }
        }
        print("DEBUG: Step 2 - Using dummy LLM data to prevent crash.") # DEBUGGING
        # --- END OF MODIFICATION ---
