import google.generativeai as genai
import os
from typing import Dict, List, Any
import json

class LLMRecommender:
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_recommendations(self, user_info: Dict[str, Any], fund_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized investment recommendations using LLM"""
        
        # Create a comprehensive prompt for the LLM
        prompt = self._create_analysis_prompt(user_info, fund_data)
        
        try:
            # Create system prompt and user prompt
            system_prompt = """You are an expert financial advisor specializing in mutual fund investments in India. 
            You provide personalized, well-reasoned investment advice based on user profiles and fund data. 
            Always consider risk tolerance, investment horizon, and financial goals. 
            Be conservative and emphasize the importance of diversification."""
            
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1500,
                    temperature=0.7
                )
            )
            
            analysis = response.text
            
            # Parse the analysis into structured format
            structured_analysis = self._parse_llm_response(analysis, user_info, fund_data)
            
            return structured_analysis
            
        except Exception as e:
            # Fallback to rule-based recommendations if LLM fails
            return self._generate_fallback_recommendations(user_info, fund_data)
    
    def _create_analysis_prompt(self, user_info: Dict[str, Any], fund_data: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for LLM analysis"""
        
        # Enhanced user profile information
        user_profile = f"""
User Profile:
- Name: {user_info.get('name', 'User')}
- Age: {user_info.get('age', 0)} years
- Annual Income: ₹{user_info.get('annual_income', 0):,.0f}
- Investment Amount: ₹{user_info.get('investment_amount', 0):,.0f}
- Risk Appetite: {user_info.get('risk_tolerance', 'moderate').title()}
- Investment Goal: {user_info.get('investment_goal', 'wealth_creation').replace('_', ' ').title()}
- Investment Horizon: {user_info.get('investment_horizon', '5-10')} years
- Monthly SIP Budget: ₹{user_info.get('monthly_sip', 0):,.0f}
- Existing Investments: ₹{user_info.get('existing_investments', 0):,.0f}
- Tax Bracket: {user_info.get('tax_bracket', 20)}%
- Emergency Fund: {user_info.get('emergency_fund', 'yes').title()}
- Fund Type Preference: {user_info.get('fund_type_preference', 'direct').title()}
- ESG Preference: {user_info.get('esg_preference', 'no_preference').replace('_', ' ').title()}
- Dividend vs Growth: {user_info.get('dividend_preference', 'growth').title()}
"""

        # Enhanced fund recommendations
        fund_recommendations = "Recommended Funds:\n"
        for category, funds in fund_data.get('recommendations', {}).items():
            fund_recommendations += f"\n{category.replace('_', ' ').title()}:\n"
            for i, fund in enumerate(funds, 1):
                fund_recommendations += f"""
{i}. {fund['name']}
   - Fund Manager: {fund['fund_manager']}
   - AUM: ₹{fund['aum_cr']:,.1f} Cr
   - Expense Ratio: {fund['expense_ratio']}%
   - 5Y SIP Return: {fund['sip_5yr_return']}%
   - 10Y SIP Return: {fund['sip_10yr_return']}%
   - Alpha: {fund['alpha']}
   - Beta: {fund['beta']}
   - Sharpe Ratio: {fund['sharpe_ratio']}
   - Sortino Ratio: {fund['sortino_ratio']}
   - ESG Score: {fund.get('esg_score', 'N/A')}/10
   - Volatility: {fund.get('volatility_rank', 'moderate').title()}
   - Peer Rank: {fund.get('peer_rank', 'N/A')}
   - Risk-Adjusted Return: {fund.get('risk_adjusted_return', 'N/A')}%
   - Diversification Score: {fund.get('diversification_score', 'N/A')}/100
"""

        # Advanced analysis data
        advanced_analysis = fund_data.get('advanced_analysis', {})
        advanced_info = ""
        
        if advanced_analysis.get('projections'):
            proj = advanced_analysis['projections']
            advanced_info += f"""
Investment Projections:
- Monthly SIP: ₹{proj.get('monthly_sip', 0):,.0f}
- Total Investment: ₹{proj.get('total_investment', 0):,.0f}
- Projected Value: ₹{proj.get('projected_value', 0):,.0f}
- Expected Return: {proj.get('expected_return', 0)}%
- Time Period: {proj.get('time_period', 0)} years
"""

        if advanced_analysis.get('diversification_score'):
            div = advanced_analysis['diversification_score']
            advanced_info += f"""
Portfolio Diversification:
- Score: {div.get('score', 0)}/150
- Categories: {div.get('categories', 0)}
- Total Funds: {div.get('total_funds', 0)}
- Assessment: {div.get('assessment', 'N/A')}
"""

        if advanced_analysis.get('expense_impact'):
            exp = advanced_analysis['expense_impact']
            advanced_info += f"""
Expense Impact Analysis:
- Average Expense Ratio: {exp.get('average_expense_ratio', 0)}%
- Total Expense Over Period: ₹{exp.get('total_expense_over_period', 0):,.0f}
- Potential Savings: ₹{exp.get('potential_savings', 0):,.0f}
- Assessment: {exp.get('impact_assessment', 'N/A')}
"""

        if advanced_analysis.get('volatility_analysis'):
            vol = advanced_analysis['volatility_analysis']
            advanced_info += f"""
Volatility Analysis:
- Volatility Breakdown: Low: {vol.get('volatility_breakdown', {}).get('low', 0)}, Moderate: {vol.get('volatility_breakdown', {}).get('moderate', 0)}, High: {vol.get('volatility_breakdown', {}).get('high', 0)}
- High Volatility Percentage: {vol.get('high_volatility_percentage', 0):.1f}%
- Risk Assessment: {vol.get('risk_assessment', 'N/A')}
"""

        if advanced_analysis.get('risk_warnings'):
            warnings = advanced_analysis['risk_warnings']
            advanced_info += f"""
Risk Warnings:
{chr(10).join(f"- {warning}" for warning in warnings)}
"""

        prompt = f"""
{user_profile}

{fund_recommendations}

{advanced_info}

Please provide a comprehensive analysis including:

1. **Executive Summary**: Brief overview of the investment strategy
2. **Risk Assessment**: Detailed risk analysis considering user's profile and selected funds
3. **Portfolio Analysis**: Analysis of diversification, expense impact, and volatility
4. **Investment Strategy**: Specific recommendations based on user's goals and preferences
5. **Key Insights**: Important considerations and next steps
6. **Risk Warnings**: Any specific risks the user should be aware of

Consider the user's:
- Investment goal and horizon
- Risk tolerance and existing investments
- Tax bracket and emergency fund status
- ESG and dividend preferences
- Advanced metrics like ESG scores, volatility rankings, and peer comparisons

Provide actionable, personalized advice that helps the user make informed investment decisions.
"""

        return prompt
    
    def _parse_llm_response(self, analysis: str, user_info: Dict, fund_data: Dict) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        
        # Extract key sections from the analysis
        sections = {
            'risk_assessment': self._extract_section(analysis, 'RISK ASSESSMENT'),
            'portfolio_allocation': self._extract_section(analysis, 'PORTFOLIO ALLOCATION'),
            'fund_analysis': self._extract_section(analysis, 'FUND SELECTION ANALYSIS'),
            'investment_strategy': self._extract_section(analysis, 'INVESTMENT STRATEGY'),
            'risk_warnings': self._extract_section(analysis, 'RISK WARNINGS'),
            'next_steps': self._extract_section(analysis, 'NEXT STEPS'),
            'full_analysis': analysis
        }
        
        # Calculate suggested allocations based on fund data
        suggested_allocations = self._calculate_suggested_allocations(user_info, fund_data)
        
        return {
            'sections': sections,
            'suggested_allocations': suggested_allocations,
            'summary': self._generate_summary(user_info, fund_data),
            'key_insights': self._extract_key_insights(analysis)
        }
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from the LLM response"""
        try:
            start_marker = f"{section_name}:"
            end_markers = ["RISK ASSESSMENT:", "PORTFOLIO ALLOCATION:", "FUND SELECTION ANALYSIS:", 
                          "INVESTMENT STRATEGY:", "RISK WARNINGS:", "NEXT STEPS:"]
            
            start_idx = text.find(start_marker)
            if start_idx == -1:
                return ""
            
            start_idx += len(start_marker)
            
            # Find the next section marker
            end_idx = len(text)
            for marker in end_markers:
                if marker != start_marker:
                    marker_idx = text.find(marker, start_idx)
                    if marker_idx != -1 and marker_idx < end_idx:
                        end_idx = marker_idx
            
            return text[start_idx:end_idx].strip()
        except:
            return ""
    
    def _calculate_suggested_allocations(self, user_info: Dict, fund_data: Dict) -> Dict[str, Any]:
        """Calculate suggested investment allocations"""
        
        total_amount = user_info['investment_amount']
        risk_profile = fund_data.get('risk_profile', 'moderate')
        allocation = fund_data.get('allocation', {})
        
        suggested_allocations = {}
        
        for category, percentage in allocation.items():
            if percentage > 0:
                amount = (percentage / 100) * total_amount
                suggested_allocations[category] = {
                    'percentage': percentage,
                    'amount': amount,
                    'funds': fund_data['recommendations'].get(category, [])
                }
        
        return suggested_allocations
    
    def _generate_summary(self, user_info: Dict, fund_data: Dict) -> str:
        """Generate a concise summary of recommendations"""
        
        risk_profile = fund_data.get('risk_profile', 'moderate')
        total_amount = user_info['investment_amount']
        
        summary = f"""
        Based on your profile (Age: {user_info['age']}, Income: ₹{user_info['annual_income']:,.0f}), 
        we've identified you as a {risk_profile} risk investor. 
        
        For your investment of ₹{total_amount:,.0f}, we recommend a diversified portfolio across 
        {len([k for k, v in fund_data.get('allocation', {}).items() if v > 0])} fund categories.
        
        Key highlights:
        - Risk Profile: {risk_profile.title()}
        - Recommended Categories: {', '.join([k.replace('_', ' ').title() for k, v in fund_data.get('allocation', {}).items() if v > 0])}
        - Investment Strategy: Diversified approach with focus on long-term growth
        """
        
        return summary.strip()
    
    def _extract_key_insights(self, analysis: str) -> List[str]:
        """Extract key insights from the LLM analysis"""
        
        insights = []
        
        # Look for key phrases that indicate important insights
        key_phrases = [
            "important to note",
            "key consideration",
            "recommend",
            "suggest",
            "consider",
            "highlight",
            "crucial",
            "essential"
        ]
        
        lines = analysis.split('\n')
        for line in lines:
            line = line.strip()
            if any(phrase in line.lower() for phrase in key_phrases) and len(line) > 20:
                insights.append(line)
        
        return insights[:5]  # Return top 5 insights
    
    def _generate_fallback_recommendations(self, user_info: Dict, fund_data: Dict) -> Dict[str, Any]:
        """Generate fallback recommendations if LLM fails"""
        
        return {
            'sections': {
                'risk_assessment': f"Based on your age ({user_info['age']}) and income (₹{user_info['annual_income']:,.0f}), you appear to be a {fund_data.get('risk_profile', 'moderate')} risk investor.",
                'portfolio_allocation': "We recommend a diversified approach across multiple fund categories to balance risk and returns.",
                'fund_analysis': "The recommended funds have been selected based on their track record, AUM, and risk-adjusted returns.",
                'investment_strategy': "Consider starting with SIP (Systematic Investment Plan) for better rupee cost averaging.",
                'risk_warnings': "Past performance does not guarantee future returns. Please consult a financial advisor before investing.",
                'next_steps': "Review the fund details, understand the risks, and start with small investments to test your comfort level.",
                'full_analysis': "Please review the detailed fund recommendations below."
            },
            'suggested_allocations': self._calculate_suggested_allocations(user_info, fund_data),
            'summary': self._generate_summary(user_info, fund_data),
            'key_insights': [
                "Diversification is key to managing investment risk",
                "Consider your investment horizon when selecting funds",
                "Regular monitoring and rebalancing is important",
                "Start with SIP for better risk management",
                "Consult a financial advisor for personalized advice"
            ]
        }
