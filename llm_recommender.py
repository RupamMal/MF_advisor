# llm_recommender.py
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables.")

genai.configure(api_key=API_KEY)

class LLMRecommender:
    def __init__(self, model="gemini-1.5-flash"):
        # Use the high-level GenerativeModel wrapper
        self.client = genai.GenerativeModel(model)

    def _build_prompt(self, user_info, recommendations):
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
        try:
            response = self.client.generate_content(prompt)
            text = response.text.strip()

            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                match = re.search(r"\{[\s\S]*\}", text)
                if match:
                    parsed = json.loads(match.group())
                else:
                    raise ValueError("No valid JSON found.")

            # Ensure structured output
            return {
                "summary": parsed.get("summary", ""),
                "key_insights": parsed.get("key_insights", []),
                "suggested_allocations": parsed.get("suggested_allocations", parsed.get("allocations", {})),
                "sections": parsed.get("sections", {})
            }

        except Exception as e:
            print(f"[LLMRecommender] Error: {e}")
            return {
                "summary": "Error generating analysis.",
                "key_insights": [],
                "suggested_allocations": recommendations.get("allocations", {}),
                "sections": {}
            }
