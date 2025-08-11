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

    def generate_recommendations(self, user_info, recommendations):
        prompt = self._build_prompt(user_info, recommendations)
        
        # --- START OF MODIFICATION: ADD ROBUST ERROR HANDLING ---
        try:
            # Generate the content
            response = self.client.generate_content(prompt)
            text = response.text.strip()

            # Attempt to parse the JSON response
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                # Common case: LLM includes markdown backticks ```json ... ```
                match = re.search(r"\{[\s\S]*\}", text)
                if match:
                    parsed = json.loads(match.group())
                else:
                    # If no JSON is found at all, raise an error to be caught below
                    raise ValueError("No valid JSON found in LLM response.")

            # Ensure the final output has a consistent structure
            return {
                "summary": parsed.get("summary", "AI analysis could not be generated."),
                "key_insights": parsed.get("key_insights", []),
                "suggested_allocations": parsed.get("suggested_allocations", parsed.get("allocations", {})),
                "sections": parsed.get("sections", {})
            }

        except Exception as e:
            # This will catch ANY error during the API call or parsing
            # and prevent the server from crashing.
            print(f"[LLMRecommender] CRITICAL ERROR: {e}")
            
            # Return a default/error structure so the frontend doesn't crash
            return {
                "summary": "We're sorry, the AI analysis could not be completed at this time. This could be due to high traffic or a temporary connection issue.",
                "key_insights": ["An error occurred while communicating with the analysis service."],
                # Fallback to basic allocations so the page still has some data
                "suggested_allocations": recommendations.get("allocations", {}),
                "sections": {
                    "error_details": f"An unexpected error occurred. Please try again later."
                }
            }
        # --- END OF MODIFICATION ---
