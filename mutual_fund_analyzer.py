import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List, Any
import yfinance as yf

class MutualFundAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Sample mutual fund data (in real implementation, this would be fetched from APIs)
        self.fund_data = self._load_sample_data()
    
    def _load_sample_data(self) -> Dict[str, List[Dict]]:
        """Load sample mutual fund data for demonstration"""
        return {
            'large_cap': [
                {
                    'id': 'LARGE_001',
                    'name': 'HDFC Top 100 Fund',
                    'aum_cr': 15420.5,
                    'expense_ratio': 1.75,
                    'sip_5yr_return': 12.8,
                    'sip_10yr_return': 14.2,
                    'alpha': 2.1,
                    'beta': 0.95,
                    'std_dev': 15.2,
                    'sharpe_ratio': 0.85,
                    'sortino_ratio': 1.12,
                    'fund_manager': 'Prashant Jain',
                    'category': 'Large Cap',
                    'nav': 45.67,
                    'min_investment': 5000,
                    'esg_score': 7.5,
                    'volatility_rank': 'low',
                    'peer_rank': 1,
                    'risk_adjusted_return': 8.9,
                    'diversification_score': 85
                },
                {
                    'id': 'LARGE_002',
                    'name': 'Axis Bluechip Fund',
                    'aum_cr': 12500.0,
                    'expense_ratio': 1.65,
                    'sip_5yr_return': 13.2,
                    'sip_10yr_return': 14.8,
                    'alpha': 2.8,
                    'beta': 0.92,
                    'std_dev': 14.8,
                    'sharpe_ratio': 0.92,
                    'sortino_ratio': 1.18,
                    'fund_manager': 'Shreyash Devalkar',
                    'category': 'Large Cap',
                    'nav': 38.45,
                    'min_investment': 5000,
                    'esg_score': 8.2,
                    'volatility_rank': 'low',
                    'peer_rank': 2,
                    'risk_adjusted_return': 9.1,
                    'diversification_score': 82
                },
                {
                    'id': 'LARGE_003',
                    'name': 'SBI Bluechip Fund',
                    'aum_cr': 9800.0,
                    'expense_ratio': 1.70,
                    'sip_5yr_return': 12.5,
                    'sip_10yr_return': 13.8,
                    'alpha': 2.3,
                    'beta': 0.94,
                    'std_dev': 15.0,
                    'sharpe_ratio': 0.88,
                    'sortino_ratio': 1.15,
                    'fund_manager': 'Sohini Andani',
                    'category': 'Large Cap',
                    'nav': 42.30,
                    'min_investment': 5000,
                    'esg_score': 7.8,
                    'volatility_rank': 'low',
                    'peer_rank': 3,
                    'risk_adjusted_return': 8.7,
                    'diversification_score': 80
                },
                {
                    'id': 'LARGE_004',
                    'name': 'ICICI Prudential Bluechip Fund',
                    'aum_cr': 11200.0,
                    'expense_ratio': 1.68,
                    'sip_5yr_return': 13.0,
                    'sip_10yr_return': 14.5,
                    'alpha': 2.5,
                    'beta': 0.93,
                    'std_dev': 14.9,
                    'sharpe_ratio': 0.90,
                    'sortino_ratio': 1.16,
                    'fund_manager': 'Manish Gunwani',
                    'category': 'Large Cap',
                    'nav': 39.80,
                    'min_investment': 5000,
                    'esg_score': 8.0,
                    'volatility_rank': 'low',
                    'peer_rank': 4,
                    'risk_adjusted_return': 9.0,
                    'diversification_score': 83
                },
                {
                    'id': 'LARGE_005',
                    'name': 'Kotak Bluechip Fund',
                    'aum_cr': 8900.0,
                    'expense_ratio': 1.72,
                    'sip_5yr_return': 12.9,
                    'sip_10yr_return': 14.1,
                    'alpha': 2.2,
                    'beta': 0.96,
                    'std_dev': 15.1,
                    'sharpe_ratio': 0.87,
                    'sortino_ratio': 1.13,
                    'fund_manager': 'Harsha Upadhyaya',
                    'category': 'Large Cap',
                    'nav': 41.20,
                    'min_investment': 5000,
                    'esg_score': 7.6,
                    'volatility_rank': 'low',
                    'peer_rank': 5,
                    'risk_adjusted_return': 8.8,
                    'diversification_score': 81
                }
            ],
            'mid_cap': [
                {
                    'id': 'MID_001',
                    'name': 'Kotak Emerging Equity Fund',
                    'aum_cr': 8500.0,
                    'expense_ratio': 1.85,
                    'sip_5yr_return': 15.2,
                    'sip_10yr_return': 16.5,
                    'alpha': 3.2,
                    'beta': 1.05,
                    'std_dev': 18.5,
                    'sharpe_ratio': 0.78,
                    'sortino_ratio': 1.05,
                    'fund_manager': 'Pankaj Tibrewal',
                    'category': 'Mid Cap',
                    'nav': 52.30,
                    'min_investment': 5000,
                    'esg_score': 6.8,
                    'volatility_rank': 'moderate',
                    'peer_rank': 1,
                    'risk_adjusted_return': 9.8,
                    'diversification_score': 78
                },
                {
                    'id': 'MID_002',
                    'name': 'Axis Midcap Fund',
                    'aum_cr': 7200.0,
                    'expense_ratio': 1.80,
                    'sip_5yr_return': 14.8,
                    'sip_10yr_return': 16.0,
                    'alpha': 3.0,
                    'beta': 1.03,
                    'std_dev': 18.0,
                    'sharpe_ratio': 0.80,
                    'sortino_ratio': 1.08,
                    'fund_manager': 'Shreyash Devalkar',
                    'category': 'Mid Cap',
                    'nav': 48.90,
                    'min_investment': 5000,
                    'esg_score': 7.2,
                    'volatility_rank': 'moderate',
                    'peer_rank': 2,
                    'risk_adjusted_return': 9.5,
                    'diversification_score': 80
                },
                {
                    'id': 'MID_003',
                    'name': 'HDFC Mid-Cap Opportunities Fund',
                    'aum_cr': 6800.0,
                    'expense_ratio': 1.88,
                    'sip_5yr_return': 15.5,
                    'sip_10yr_return': 16.8,
                    'alpha': 3.5,
                    'beta': 1.08,
                    'std_dev': 19.2,
                    'sharpe_ratio': 0.75,
                    'sortino_ratio': 1.02,
                    'fund_manager': 'Chirag Setalvad',
                    'category': 'Mid Cap',
                    'nav': 55.40,
                    'min_investment': 5000,
                    'esg_score': 6.5,
                    'volatility_rank': 'moderate',
                    'peer_rank': 3,
                    'risk_adjusted_return': 10.1,
                    'diversification_score': 75
                },
                {
                    'id': 'MID_004',
                    'name': 'SBI Magnum Midcap Fund',
                    'aum_cr': 5900.0,
                    'expense_ratio': 1.82,
                    'sip_5yr_return': 14.2,
                    'sip_10yr_return': 15.5,
                    'alpha': 2.8,
                    'beta': 1.02,
                    'std_dev': 17.8,
                    'sharpe_ratio': 0.82,
                    'sortino_ratio': 1.10,
                    'fund_manager': 'Sohini Andani',
                    'category': 'Mid Cap',
                    'nav': 46.70,
                    'min_investment': 5000,
                    'esg_score': 7.0,
                    'volatility_rank': 'moderate',
                    'peer_rank': 4,
                    'risk_adjusted_return': 9.2,
                    'diversification_score': 82
                },
                {
                    'id': 'MID_005',
                    'name': 'ICICI Prudential Midcap Fund',
                    'aum_cr': 6300.0,
                    'expense_ratio': 1.85,
                    'sip_5yr_return': 14.9,
                    'sip_10yr_return': 16.2,
                    'alpha': 3.1,
                    'beta': 1.06,
                    'std_dev': 18.8,
                    'sharpe_ratio': 0.77,
                    'sortino_ratio': 1.04,
                    'fund_manager': 'Manish Gunwani',
                    'category': 'Mid Cap',
                    'nav': 51.20,
                    'min_investment': 5000,
                    'esg_score': 6.9,
                    'volatility_rank': 'moderate',
                    'peer_rank': 5,
                    'risk_adjusted_return': 9.6,
                    'diversification_score': 77
                }
            ],
            'flexi_cap': [
                {
                    'id': 'FLEXI_001',
                    'name': 'ICICI Prudential Flexi Cap Fund',
                    'aum_cr': 12000.0,
                    'expense_ratio': 1.70,
                    'sip_5yr_return': 14.5,
                    'sip_10yr_return': 15.8,
                    'alpha': 2.5,
                    'beta': 0.98,
                    'std_dev': 16.2,
                    'sharpe_ratio': 0.88,
                    'sortino_ratio': 1.15,
                    'fund_manager': 'Sankaran Naren',
                    'category': 'Flexi Cap',
                    'nav': 41.20,
                    'min_investment': 5000,
                    'esg_score': 7.8,
                    'volatility_rank': 'moderate',
                    'peer_rank': 1,
                    'risk_adjusted_return': 9.3,
                    'diversification_score': 90
                },
                {
                    'id': 'FLEXI_002',
                    'name': 'Axis Flexi Cap Fund',
                    'aum_cr': 9800.0,
                    'expense_ratio': 1.68,
                    'sip_5yr_return': 14.8,
                    'sip_10yr_return': 16.1,
                    'alpha': 2.8,
                    'beta': 0.99,
                    'std_dev': 16.5,
                    'sharpe_ratio': 0.90,
                    'sortino_ratio': 1.18,
                    'fund_manager': 'Shreyash Devalkar',
                    'category': 'Flexi Cap',
                    'nav': 43.80,
                    'min_investment': 5000,
                    'esg_score': 8.0,
                    'volatility_rank': 'moderate',
                    'peer_rank': 2,
                    'risk_adjusted_return': 9.6,
                    'diversification_score': 88
                },
                {
                    'id': 'FLEXI_003',
                    'name': 'HDFC Flexi Cap Fund',
                    'aum_cr': 10500.0,
                    'expense_ratio': 1.72,
                    'sip_5yr_return': 14.2,
                    'sip_10yr_return': 15.5,
                    'alpha': 2.3,
                    'beta': 0.97,
                    'std_dev': 15.9,
                    'sharpe_ratio': 0.86,
                    'sortino_ratio': 1.12,
                    'fund_manager': 'Prashant Jain',
                    'category': 'Flexi Cap',
                    'nav': 40.50,
                    'min_investment': 5000,
                    'esg_score': 7.6,
                    'volatility_rank': 'moderate',
                    'peer_rank': 3,
                    'risk_adjusted_return': 9.1,
                    'diversification_score': 85
                },
                {
                    'id': 'FLEXI_004',
                    'name': 'SBI Flexi Cap Fund',
                    'aum_cr': 8200.0,
                    'expense_ratio': 1.75,
                    'sip_5yr_return': 14.0,
                    'sip_10yr_return': 15.3,
                    'alpha': 2.1,
                    'beta': 0.96,
                    'std_dev': 15.7,
                    'sharpe_ratio': 0.84,
                    'sortino_ratio': 1.10,
                    'fund_manager': 'Sohini Andani',
                    'category': 'Flexi Cap',
                    'nav': 38.90,
                    'min_investment': 5000,
                    'esg_score': 7.4,
                    'volatility_rank': 'moderate',
                    'peer_rank': 4,
                    'risk_adjusted_return': 8.9,
                    'diversification_score': 87
                },
                {
                    'id': 'FLEXI_005',
                    'name': 'Kotak Flexi Cap Fund',
                    'aum_cr': 7500.0,
                    'expense_ratio': 1.73,
                    'sip_5yr_return': 14.6,
                    'sip_10yr_return': 15.9,
                    'alpha': 2.6,
                    'beta': 0.98,
                    'std_dev': 16.3,
                    'sharpe_ratio': 0.89,
                    'sortino_ratio': 1.16,
                    'fund_manager': 'Harsha Upadhyaya',
                    'category': 'Flexi Cap',
                    'nav': 42.10,
                    'min_investment': 5000,
                    'esg_score': 7.9,
                    'volatility_rank': 'moderate',
                    'peer_rank': 5,
                    'risk_adjusted_return': 9.4,
                    'diversification_score': 86
                }
            ],
            'small_cap': [
                {
                    'id': 'SMALL_001',
                    'name': 'SBI Small Cap Fund',
                    'aum_cr': 6500.0,
                    'expense_ratio': 1.95,
                    'sip_5yr_return': 18.5,
                    'sip_10yr_return': 20.2,
                    'alpha': 4.2,
                    'beta': 1.15,
                    'std_dev': 22.5,
                    'sharpe_ratio': 0.72,
                    'sortino_ratio': 0.95,
                    'fund_manager': 'R Srinivasan',
                    'category': 'Small Cap',
                    'nav': 28.75,
                    'min_investment': 5000,
                    'esg_score': 5.5,
                    'volatility_rank': 'high',
                    'peer_rank': 1,
                    'risk_adjusted_return': 11.2,
                    'diversification_score': 65
                },
                {
                    'id': 'SMALL_002',
                    'name': 'Axis Small Cap Fund',
                    'aum_cr': 5200.0,
                    'expense_ratio': 1.90,
                    'sip_5yr_return': 19.2,
                    'sip_10yr_return': 21.0,
                    'alpha': 4.8,
                    'beta': 1.18,
                    'std_dev': 23.8,
                    'sharpe_ratio': 0.68,
                    'sortino_ratio': 0.92,
                    'fund_manager': 'Shreyash Devalkar',
                    'category': 'Small Cap',
                    'nav': 32.40,
                    'min_investment': 5000,
                    'esg_score': 5.8,
                    'volatility_rank': 'high',
                    'peer_rank': 2,
                    'risk_adjusted_return': 11.8,
                    'diversification_score': 62
                },
                {
                    'id': 'SMALL_003',
                    'name': 'HDFC Small Cap Fund',
                    'aum_cr': 4800.0,
                    'expense_ratio': 1.98,
                    'sip_5yr_return': 17.8,
                    'sip_10yr_return': 19.5,
                    'alpha': 3.9,
                    'beta': 1.12,
                    'std_dev': 21.8,
                    'sharpe_ratio': 0.75,
                    'sortino_ratio': 0.98,
                    'fund_manager': 'Chirag Setalvad',
                    'category': 'Small Cap',
                    'nav': 26.90,
                    'min_investment': 5000,
                    'esg_score': 5.2,
                    'volatility_rank': 'high',
                    'peer_rank': 3,
                    'risk_adjusted_return': 10.8,
                    'diversification_score': 68
                },
                {
                    'id': 'SMALL_004',
                    'name': 'ICICI Prudential Small Cap Fund',
                    'aum_cr': 4100.0,
                    'expense_ratio': 1.92,
                    'sip_5yr_return': 18.0,
                    'sip_10yr_return': 19.8,
                    'alpha': 4.0,
                    'beta': 1.14,
                    'std_dev': 22.2,
                    'sharpe_ratio': 0.73,
                    'sortino_ratio': 0.96,
                    'fund_manager': 'Manish Gunwani',
                    'category': 'Small Cap',
                    'nav': 29.50,
                    'min_investment': 5000,
                    'esg_score': 5.6,
                    'volatility_rank': 'high',
                    'peer_rank': 4,
                    'risk_adjusted_return': 11.0,
                    'diversification_score': 66
                },
                {
                    'id': 'SMALL_005',
                    'name': 'Kotak Small Cap Fund',
                    'aum_cr': 3800.0,
                    'expense_ratio': 1.88,
                    'sip_5yr_return': 17.5,
                    'sip_10yr_return': 19.2,
                    'alpha': 3.7,
                    'beta': 1.10,
                    'std_dev': 21.5,
                    'sharpe_ratio': 0.76,
                    'sortino_ratio': 0.99,
                    'fund_manager': 'Pankaj Tibrewal',
                    'category': 'Small Cap',
                    'nav': 25.80,
                    'min_investment': 5000,
                    'esg_score': 5.4,
                    'volatility_rank': 'high',
                    'peer_rank': 5,
                    'risk_adjusted_return': 10.6,
                    'diversification_score': 70
                }
            ],
            'multi_cap': [
                {
                    'id': 'MULTI_001',
                    'name': 'Nippon India Multi Cap Fund',
                    'aum_cr': 7500.0,
                    'expense_ratio': 1.80,
                    'sip_5yr_return': 13.8,
                    'sip_10yr_return': 15.2,
                    'alpha': 2.8,
                    'beta': 1.02,
                    'std_dev': 17.0,
                    'sharpe_ratio': 0.82,
                    'sortino_ratio': 1.08,
                    'fund_manager': 'Sailesh Raj Bhan',
                    'category': 'Multi Cap',
                    'nav': 35.60,
                    'min_investment': 5000,
                    'esg_score': 7.2,
                    'volatility_rank': 'moderate',
                    'peer_rank': 1,
                    'risk_adjusted_return': 9.0,
                    'diversification_score': 88
                },
                {
                    'id': 'MULTI_002',
                    'name': 'Axis Multi Cap Fund',
                    'aum_cr': 6800.0,
                    'expense_ratio': 1.75,
                    'sip_5yr_return': 14.2,
                    'sip_10yr_return': 15.6,
                    'alpha': 3.0,
                    'beta': 1.04,
                    'std_dev': 17.5,
                    'sharpe_ratio': 0.85,
                    'sortino_ratio': 1.12,
                    'fund_manager': 'Shreyash Devalkar',
                    'category': 'Multi Cap',
                    'nav': 38.20,
                    'min_investment': 5000,
                    'esg_score': 7.5,
                    'volatility_rank': 'moderate',
                    'peer_rank': 2,
                    'risk_adjusted_return': 9.3,
                    'diversification_score': 85
                },
                {
                    'id': 'MULTI_003',
                    'name': 'HDFC Multi Cap Fund',
                    'aum_cr': 6200.0,
                    'expense_ratio': 1.78,
                    'sip_5yr_return': 13.5,
                    'sip_10yr_return': 14.9,
                    'alpha': 2.6,
                    'beta': 1.01,
                    'std_dev': 16.8,
                    'sharpe_ratio': 0.80,
                    'sortino_ratio': 1.06,
                    'fund_manager': 'Prashant Jain',
                    'category': 'Multi Cap',
                    'nav': 34.80,
                    'min_investment': 5000,
                    'esg_score': 7.0,
                    'volatility_rank': 'moderate',
                    'peer_rank': 3,
                    'risk_adjusted_return': 8.7,
                    'diversification_score': 90
                },
                {
                    'id': 'MULTI_004',
                    'name': 'SBI Multi Cap Fund',
                    'aum_cr': 5400.0,
                    'expense_ratio': 1.82,
                    'sip_5yr_return': 13.2,
                    'sip_10yr_return': 14.6,
                    'alpha': 2.4,
                    'beta': 1.00,
                    'std_dev': 16.5,
                    'sharpe_ratio': 0.78,
                    'sortino_ratio': 1.04,
                    'fund_manager': 'Sohini Andani',
                    'category': 'Multi Cap',
                    'nav': 32.40,
                    'min_investment': 5000,
                    'esg_score': 6.8,
                    'volatility_rank': 'moderate',
                    'peer_rank': 4,
                    'risk_adjusted_return': 8.5,
                    'diversification_score': 92
                },
                {
                    'id': 'MULTI_005',
                    'name': 'ICICI Prudential Multi Cap Fund',
                    'aum_cr': 5800.0,
                    'expense_ratio': 1.77,
                    'sip_5yr_return': 13.9,
                    'sip_10yr_return': 15.3,
                    'alpha': 2.7,
                    'beta': 1.03,
                    'std_dev': 17.2,
                    'sharpe_ratio': 0.83,
                    'sortino_ratio': 1.10,
                    'fund_manager': 'Manish Gunwani',
                    'category': 'Multi Cap',
                    'nav': 36.90,
                    'min_investment': 5000,
                    'esg_score': 7.3,
                    'volatility_rank': 'moderate',
                    'peer_rank': 5,
                    'risk_adjusted_return': 8.9,
                    'diversification_score': 87
                }
            ]
        }
    
    def get_recommendations(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get personalized mutual fund recommendations"""
        # Calculate risk profile
        risk_profile = self._calculate_risk_profile(user_info)
        
        # Get allocation suggestions
        allocation = self._suggest_allocation(user_info, risk_profile)
        
        # Get recommendations for each category
        recommendations = {}
        for category, percentage in allocation.items():
            if percentage > 0:
                funds = self.fund_data.get(category, [])
                filtered_funds = self._filter_and_rank_funds(funds, user_info, risk_profile)
                recommendations[category] = filtered_funds[:2]  # Top 2 funds per category
        
        return {
            'risk_profile': risk_profile,
            'allocation': allocation,
            'recommendations': recommendations,
            'advanced_analysis': self._generate_advanced_analysis(user_info, recommendations, allocation)
        }
    
    def _generate_advanced_analysis(self, user_info: Dict, recommendations: Dict, allocation: Dict) -> Dict:
        """Generate advanced analysis including projections, diversification, etc."""
        return {
            'projections': self._calculate_projections(user_info),
            'diversification_score': self._calculate_diversification_score(recommendations),
            'expense_impact': self._calculate_expense_impact(recommendations, user_info),
            'volatility_analysis': self._analyze_volatility(recommendations),
            'peer_comparison': self._generate_peer_comparison(recommendations),
            'risk_warnings': self._generate_risk_warnings(recommendations, user_info)
        }
    
    def _calculate_projections(self, user_info: Dict) -> Dict:
        """Calculate investment projections"""
        monthly_sip = user_info.get('monthly_sip', 0)
        investment_horizon = self._parse_horizon(user_info.get('investment_horizon', '5-10'))
        expected_return = 12.0  # Conservative estimate
        
        if monthly_sip > 0:
            # SIP projection formula
            total_investment = monthly_sip * 12 * investment_horizon
            projected_value = monthly_sip * ((((1 + expected_return/100) ** (investment_horizon * 12)) - 1) / (expected_return/100)) * (1 + expected_return/100)
            
            return {
                'monthly_sip': monthly_sip,
                'total_investment': total_investment,
                'projected_value': projected_value,
                'expected_return': expected_return,
                'time_period': investment_horizon
            }
        return {}
    
    def _parse_horizon(self, horizon: str) -> int:
        """Parse investment horizon string to years"""
        if '1-3' in horizon: return 2
        elif '3-5' in horizon: return 4
        elif '5-10' in horizon: return 7
        elif '10-15' in horizon: return 12
        elif '15+' in horizon: return 20
        return 7  # default
    
    def _calculate_diversification_score(self, recommendations: Dict) -> Dict:
        """Calculate portfolio diversification score"""
        total_funds = sum(len(funds) for funds in recommendations.values())
        categories = len(recommendations)
        
        # Base score on number of categories and funds
        category_score = min(categories * 20, 100)  # Max 100 for 5+ categories
        fund_score = min(total_funds * 10, 50)  # Max 50 for 5+ funds
        
        total_score = category_score + fund_score
        
        return {
            'score': total_score,
            'categories': categories,
            'total_funds': total_funds,
            'assessment': self._get_diversification_assessment(total_score)
        }
    
    def _get_diversification_assessment(self, score: float) -> str:
        if score >= 120: return "Excellent - Well diversified across categories"
        elif score >= 100: return "Good - Balanced diversification"
        elif score >= 80: return "Moderate - Some concentration risk"
        else: return "Limited - Consider adding more categories"
    
    def _calculate_expense_impact(self, recommendations: Dict, user_info: Dict) -> Dict:
        """Calculate impact of expense ratios on returns"""
        all_funds = []
        for funds in recommendations.values():
            all_funds.extend(funds)
        
        if not all_funds:
            return {}
        
        avg_expense = sum(fund['expense_ratio'] for fund in all_funds) / len(all_funds)
        investment_amount = user_info.get('investment_amount', 100000)
        investment_horizon = self._parse_horizon(user_info.get('investment_horizon', '5-10'))
        
        # Calculate expense impact over time
        annual_expense = (avg_expense / 100) * investment_amount
        total_expense = annual_expense * investment_horizon
        
        # Compare with lower expense fund (1.5%)
        lower_expense_annual = (1.5 / 100) * investment_amount
        lower_expense_total = lower_expense_annual * investment_horizon
        savings = total_expense - lower_expense_total
        
        return {
            'average_expense_ratio': avg_expense,
            'total_expense_over_period': total_expense,
            'potential_savings': savings,
            'impact_assessment': self._get_expense_impact_assessment(avg_expense)
        }
    
    def _get_expense_impact_assessment(self, expense: float) -> str:
        if expense <= 1.5: return "Excellent - Low cost funds"
        elif expense <= 2.0: return "Good - Reasonable costs"
        elif expense <= 2.5: return "Moderate - Higher than average costs"
        else: return "High - Consider lower cost alternatives"
    
    def _analyze_volatility(self, recommendations: Dict) -> Dict:
        """Analyze portfolio volatility"""
        all_funds = []
        for funds in recommendations.values():
            all_funds.extend(funds)
        
        if not all_funds:
            return {}
        
        volatility_counts = {'low': 0, 'moderate': 0, 'high': 0}
        for fund in all_funds:
            volatility_counts[fund.get('volatility_rank', 'moderate')] += 1
        
        total_funds = len(all_funds)
        high_volatility_pct = (volatility_counts['high'] / total_funds) * 100
        
        return {
            'volatility_breakdown': volatility_counts,
            'high_volatility_percentage': high_volatility_pct,
            'risk_assessment': self._get_volatility_assessment(high_volatility_pct)
        }
    
    def _get_volatility_assessment(self, high_vol_pct: float) -> str:
        if high_vol_pct == 0: return "Low volatility portfolio - Stable returns expected"
        elif high_vol_pct <= 25: return "Moderate volatility - Some fluctuation expected"
        elif high_vol_pct <= 50: return "Higher volatility - Significant fluctuations possible"
        else: return "High volatility - Be prepared for large swings"
    
    def _generate_peer_comparison(self, recommendations: Dict) -> Dict:
        """Generate peer comparison analysis"""
        comparisons = {}
        
        for category, funds in recommendations.items():
            if funds:
                top_fund = funds[0]
                comparisons[category] = {
                    'fund_name': top_fund['name'],
                    'peer_rank': top_fund.get('peer_rank', 1),
                    'risk_adjusted_return': top_fund.get('risk_adjusted_return', 0),
                    'esg_score': top_fund.get('esg_score', 0),
                    'diversification_score': top_fund.get('diversification_score', 0),
                    'why_better': self._generate_why_better_text(top_fund)
                }
        
        return comparisons
    
    def _generate_why_better_text(self, fund: Dict) -> str:
        """Generate explanation of why this fund is recommended"""
        reasons = []
        
        if fund.get('peer_rank', 10) <= 3:
            reasons.append(f"Top {fund['peer_rank']} in its category")
        
        if fund.get('risk_adjusted_return', 0) > 8:
            reasons.append("Excellent risk-adjusted returns")
        
        if fund.get('esg_score', 0) > 7:
            reasons.append("Strong ESG compliance")
        
        if fund.get('diversification_score', 0) > 80:
            reasons.append("Well-diversified portfolio")
        
        if fund.get('expense_ratio', 3) < 2:
            reasons.append("Competitive expense ratio")
        
        return "; ".join(reasons) if reasons else "Balanced performance across key metrics"
    
    def _generate_risk_warnings(self, recommendations: Dict, user_info: Dict) -> List[str]:
        """Generate risk warnings for high-risk funds"""
        warnings = []
        
        for category, funds in recommendations.items():
            for fund in funds:
                if fund.get('volatility_rank') == 'high':
                    warnings.append(f"⚠️ {fund['name']} is a high-volatility fund. Be prepared for significant price fluctuations.")
                
                if fund.get('std_dev', 0) > 20:
                    warnings.append(f"⚠️ {fund['name']} has high standard deviation ({fund['std_dev']}%). Higher risk of losses.")
                
                if category == 'small_cap' and user_info.get('risk_tolerance') == 'low':
                    warnings.append(f"⚠️ {fund['name']} is a small-cap fund, which may not suit conservative investors.")
        
        return warnings
    
    def _calculate_risk_profile(self, user_info: Dict[str, Any]) -> str:
        """Calculate risk profile based on user information"""
        age = user_info['age']
        income = user_info['annual_income']
        investment_amount = user_info['investment_amount']
        risk_tolerance = user_info.get('risk_tolerance', 'moderate')
        
        # Base risk based on age
        if age < 30:
            base_risk = 'high'
        elif age < 50:
            base_risk = 'moderate'
        else:
            base_risk = 'low'
        
        # Adjust based on income level
        if income < 500000:  # Less than 5 lakhs
            income_risk = 'low'
        elif income < 1500000:  # 5-15 lakhs
            income_risk = 'moderate'
        else:  # Above 15 lakhs
            income_risk = 'high'
        
        # Adjust based on investment amount relative to income
        investment_ratio = investment_amount / income if income > 0 else 0
        
        if investment_ratio > 0.5:  # Investing more than 50% of income
            investment_risk = 'low'  # Conservative approach
        elif investment_ratio > 0.2:  # Investing 20-50% of income
            investment_risk = 'moderate'
        else:  # Investing less than 20% of income
            investment_risk = 'high'  # Can afford to take more risk
        
        # Combine factors with user's stated risk tolerance
        risk_factors = [base_risk, income_risk, investment_risk]
        
        # Count risk levels
        risk_counts = {'low': 0, 'moderate': 0, 'high': 0}
        for risk in risk_factors:
            risk_counts[risk] += 1
        
        # Determine final risk profile
        if risk_tolerance == 'low':
            final_risk = 'low'
        elif risk_tolerance == 'high':
            final_risk = 'high'
        else:  # moderate
            # Use majority of calculated factors
            if risk_counts['high'] >= 2:
                final_risk = 'high'
            elif risk_counts['low'] >= 2:
                final_risk = 'low'
            else:
                final_risk = 'moderate'
        
        return final_risk
    
    def _filter_and_rank_funds(self, funds: List[Dict], user_info: Dict, risk_profile: str) -> List[Dict]:
        """Filter and rank funds based on user profile and risk tolerance"""
        filtered_funds = []
        
        for fund in funds:
            # Calculate composite score
            score = self._calculate_fund_score(fund, risk_profile)
            fund['score'] = score
            filtered_funds.append(fund)
        
        # Sort by score (higher is better)
        filtered_funds.sort(key=lambda x: x['score'], reverse=True)
        
        return filtered_funds
    
    def _calculate_fund_score(self, fund: Dict, risk_profile: str) -> float:
        """Calculate a composite score for a fund"""
        # Weighted scoring based on multiple factors
        weights = {
            'aum': 0.15,
            'expense_ratio': 0.10,
            'returns_5yr': 0.25,
            'returns_10yr': 0.20,
            'alpha': 0.10,
            'sharpe': 0.10,
            'sortino': 0.10
        }
        
        # Normalize values (assuming reasonable ranges)
        aum_score = min(fund['aum_cr'] / 20000, 1.0)  # Cap at 20,000 cr
        expense_score = max(0, (3.0 - fund['expense_ratio']) / 2.0)  # Lower is better
        returns_5yr_score = min(fund['sip_5yr_return'] / 20, 1.0)  # Cap at 20%
        returns_10yr_score = min(fund['sip_10yr_return'] / 20, 1.0)  # Cap at 20%
        alpha_score = min(max(fund['alpha'] / 5, 0), 1.0)  # -5 to +5 range
        sharpe_score = min(max(fund['sharpe_ratio'] / 2, 0), 1.0)  # 0 to 2 range
        sortino_score = min(max(fund['sortino_ratio'] / 2, 0), 1.0)  # 0 to 2 range
        
        # Calculate weighted score
        score = (
            weights['aum'] * aum_score +
            weights['expense_ratio'] * expense_score +
            weights['returns_5yr'] * returns_5yr_score +
            weights['returns_10yr'] * returns_10yr_score +
            weights['alpha'] * alpha_score +
            weights['sharpe'] * sharpe_score +
            weights['sortino'] * sortino_score
        )
        
        return score
    
    def _suggest_allocation(self, user_info: Dict, risk_profile: str) -> Dict[str, float]:
        """Suggest allocation percentages based on risk profile"""
        if risk_profile == 'low':
            return {
                'large_cap': 50,
                'mid_cap': 30,
                'flexi_cap': 20,
                'small_cap': 0,
                'multi_cap': 0
            }
        elif risk_profile == 'moderate':
            return {
                'large_cap': 35,
                'mid_cap': 25,
                'flexi_cap': 25,
                'small_cap': 10,
                'multi_cap': 5
            }
        else:  # high risk
            return {
                'large_cap': 25,
                'mid_cap': 20,
                'flexi_cap': 20,
                'small_cap': 20,
                'multi_cap': 15
            }
    
    def get_fund_details(self, fund_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific fund"""
        for category in self.fund_data.values():
            for fund in category:
                if fund['id'] == fund_id:
                    return fund
        return None
    
    def get_grow_url(self, fund_name: str) -> str:
        """Generate GROW website URL for a mutual fund"""
        # GROW website URL structure: https://groww.in/mutual-funds/[fund-name]
        # Convert fund name to URL-friendly format
        fund_name_clean = fund_name.lower()
        fund_name_clean = fund_name_clean.replace(' ', '-')
        fund_name_clean = fund_name_clean.replace('(', '')
        fund_name_clean = fund_name_clean.replace(')', '')
        fund_name_clean = fund_name_clean.replace('.', '')
        fund_name_clean = fund_name_clean.replace(',', '')
        fund_name_clean = fund_name_clean.replace('&', 'and')
        
        # Remove common words that might not be in the URL
        fund_name_clean = fund_name_clean.replace('fund', '')
        fund_name_clean = fund_name_clean.replace('direct', '')
        fund_name_clean = fund_name_clean.replace('growth', '')
        fund_name_clean = fund_name_clean.replace('option', '')
        
        # Clean up multiple dashes
        fund_name_clean = '-'.join(filter(None, fund_name_clean.split('-')))
        
        return f"https://groww.in/mutual-funds/{fund_name_clean}"

    def get_top_funds(self, category: str) -> List[Dict[str, Any]]:
        """Get top 5 funds for a specific category based on performance metrics"""
        try:
            # Get all funds for the category
            all_funds = self._get_funds_by_category(category)
            
            if not all_funds:
                return []
            
            # Calculate composite score for each fund
            for fund in all_funds:
                fund['score'] = self._calculate_composite_score(fund)
            
            # Sort by score in descending order and return top 5
            top_funds = sorted(all_funds, key=lambda x: x['score'], reverse=True)[:5]
            
            # Add GROW URLs
            for fund in top_funds:
                fund['grow_url'] = self.get_grow_url(fund['name'])
            
            return top_funds
            
        except Exception as e:
            print(f"Error getting top funds for {category}: {e}")
            return []

    def _get_funds_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all funds for a specific category"""
        try:
            # Load sample data
            sample_data = self._load_sample_data()
            
            # Map category names to sample data keys
            category_mapping = {
                'large_cap': 'large_cap',
                'mid_cap': 'mid_cap', 
                'flexi_cap': 'flexi_cap',
                'small_cap': 'small_cap',
                'multi_cap': 'multi_cap'
            }
            
            mapped_category = category_mapping.get(category, 'large_cap')
            return sample_data.get(mapped_category, [])
            
        except Exception as e:
            print(f"Error getting funds by category {category}: {e}")
            return []

    def _calculate_composite_score(self, fund: Dict[str, Any]) -> float:
        """Calculate a composite score based on multiple metrics"""
        try:
            # Normalize metrics to 0-100 scale
            aum_score = min(fund.get('aum_cr', 0) / 1000, 100)  # Cap at 100K Cr
            expense_score = max(0, 100 - fund.get('expense_ratio', 0) * 10)  # Lower expense is better
            sip_5yr_score = min(fund.get('sip_5yr_return', 0), 100)
            sip_10yr_score = min(fund.get('sip_10yr_return', 0), 100)
            alpha_score = max(0, min(fund.get('alpha', 0) + 50, 100))  # Normalize alpha
            sharpe_score = max(0, min(fund.get('sharpe_ratio', 0) * 20, 100))  # Normalize Sharpe
            sortino_score = max(0, min(fund.get('sortino_ratio', 0) * 20, 100))  # Normalize Sortino
            
            # Weighted average (you can adjust weights based on importance)
            weights = {
                'aum': 0.15,
                'expense': 0.10,
                'sip_5yr': 0.20,
                'sip_10yr': 0.20,
                'alpha': 0.15,
                'sharpe': 0.10,
                'sortino': 0.10
            }
            
            composite_score = (
                aum_score * weights['aum'] +
                expense_score * weights['expense'] +
                sip_5yr_score * weights['sip_5yr'] +
                sip_10yr_score * weights['sip_10yr'] +
                alpha_score * weights['alpha'] +
                sharpe_score * weights['sharpe'] +
                sortino_score * weights['sortino']
            )
            
            return round(composite_score, 2)
            
        except Exception as e:
            print(f"Error calculating composite score: {e}")
            return 0.0
    
    def fetch_live_data(self):
        """Fetch live data from financial APIs (placeholder for real implementation)"""
        # This would integrate with real APIs like:
        # - AMFI API
        # - TickerTape API
        # - MoneyControl API
        # - Yahoo Finance API
        
        pass
