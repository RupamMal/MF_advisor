import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
import traceback

load_dotenv()

class LLMRecommender:
    def __init__(self, model="gemini-1.5-flash"):
        print("DEBUG: Initializing LLMRecommender...")
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("CRITICAL LLM ERROR: GEMINI_API_KEY is not set. The recommender will not work.")
            # We don't raise an error here to allow the app to start
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(model)
                print("OK: LLMRecommender configured successfully.")
            except Exception as e:
                print(f"CRITICAL LLM ERROR: Failed to configure Gemini. Error: {e}")
                self.client = None

    def generate_recommendations(self, user_info, recommendations):
        # This function will only be called if we re-enable it in app.py
        if not self.client:
            return {"summary": "AI Recommender is not configured due to a startup error."}
        
        prompt = self._build_prompt(user_info, recommendations)
        try:
            response = self.client.generate_content(prompt)
            # ... parsing logic ...
            return json.loads(response.text)
        except Exception as e:
            error_traceback_string = traceback.format_exc()
            print("--- A CRASH OCCURRED IN LLMRecommender ---")
            print(error_traceback_string)
            return {
                "summary": "AI analysis failed.",
                "key_insights": [f"Error: {e}"],
                "suggested_allocations": recommendations.get("allocations", {}),
                "sections": {}
            }

    def _build_prompt(self, user_info, recommendations):
        # This function is fine as-is
        return f"User info: {json.dumps(user_info)}. Recommendations: {json.dumps(recommendations)}. Respond with JSON."
