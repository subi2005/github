#!/usr/bin/env python3
"""
AI-Driven Intervention Recommendations
Analyzes patient risk factors and suggests personalized preventive care actions
"""

import re
from typing import List, Dict

class InterventionRecommender:
    """AI-driven intervention recommendation system"""
    
    def __init__(self):
        # Define intervention mappings based on risk factors
        self.intervention_map = {
            # Age-related interventions
            'AGE': {
                'high_risk': [
                    "Schedule comprehensive geriatric assessment",
                    "Review medication for age-appropriate dosing",
                    "Implement fall prevention measures"
                ],
                'moderate_risk': [
                    "Annual wellness visit recommended",
                    "Review preventive care schedule"
                ]
            },
            
            # Chronic conditions
            'ALZHEIMER': [
                "Neurological consultation for cognitive assessment",
                "Implement memory support strategies",
                "Review medication interactions"
            ],
            'HEARTFAILURE': [
                "Cardiology consultation for heart failure management",
                "Implement sodium-restricted diet",
                "Daily weight monitoring recommended"
            ],
            'CANCER': [
                "Oncology consultation for treatment optimization",
                "Implement pain management strategies",
                "Nutrition support consultation"
            ],
            'PULMONARY': [
                "Pulmonology consultation for respiratory optimization",
                "Implement breathing exercises",
                "Smoking cessation support if applicable"
            ],
            'OSTEOPOROSIS': [
                "Bone density assessment and calcium supplementation",
                "Fall prevention and balance training",
                "Vitamin D supplementation review"
            ],
            'RHEUMATOID': [
                "Rheumatology consultation for disease management",
                "Implement joint protection strategies",
                "Pain management optimization"
            ],
            'STROKE': [
                "Neurology consultation for stroke prevention",
                "Implement blood pressure monitoring",
                "Anticoagulation therapy review"
            ],
            'RENAL_DISEASE': [
                "Nephrology consultation for kidney function optimization",
                "Implement renal diet restrictions",
                "Medication dose adjustment for renal function"
            ],
            
            # Clinical measures
            'BMI': {
                'high': [
                    "Nutrition consultation for weight management",
                    "Implement physical activity program",
                    "Metabolic syndrome screening"
                ],
                'low': [
                    "Nutrition consultation for weight gain",
                    "Screening for underlying conditions",
                    "Implement strength training program"
                ]
            },
            'BP_S': {
                'high': [
                    "Implement blood pressure monitoring",
                    "Cardiology consultation for hypertension management",
                    "Lifestyle modification counseling"
                ],
                'low': [
                    "Monitor for orthostatic hypotension",
                    "Review medications for blood pressure effects",
                    "Implement gradual position changes"
                ]
            },
            'GLUCOSE': {
                'high': [
                    "Endocrinology consultation for diabetes management",
                    "Implement blood glucose monitoring",
                    "Diabetes education and lifestyle counseling"
                ]
            },
            'HbA1c': {
                'high': [
                    "Diabetes management optimization",
                    "Implement glycemic control strategies",
                    "Nutrition consultation for diabetes"
                ]
            },
            'CHOLESTEROL': {
                'high': [
                    "Cardiology consultation for lipid management",
                    "Implement heart-healthy diet",
                    "Exercise program for cardiovascular health"
                ]
            },
            
            # Healthcare utilization
            'TOTAL_CLAIMS_COST': {
                'high': [
                    "Care coordination to optimize resource utilization",
                    "Review for unnecessary healthcare services",
                    "Implement preventive care strategies"
                ]
            },
            'IN_ADM': {
                'high': [
                    "Care transition planning to prevent readmissions",
                    "Post-discharge follow-up scheduling",
                    "Medication reconciliation review"
                ]
            },
            'OUT_VISITS': {
                'high': [
                    "Care coordination to optimize outpatient visits",
                    "Implement telehealth options where appropriate",
                    "Review appointment scheduling efficiency"
                ]
            },
            'ED_VISITS': {
                'high': [
                    "Implement urgent care alternatives",
                    "Care coordination to prevent ED visits",
                    "Review for appropriate care setting utilization"
                ]
            },
            'RX_ADH': {
                'low': [
                    "Medication adherence counseling",
                    "Implement medication reminder systems",
                    "Review for medication simplification"
                ]
            }
        }
        
        # Risk level thresholds
        self.risk_thresholds = {
            'AGE': {'high_risk': 75, 'moderate_risk': 65},
            'BMI': {'high': 30, 'low': 18.5},
            'BP_S': {'high': 140, 'low': 90},
            'GLUCOSE': {'high': 126},
            'HbA1c': {'high': 6.5},
            'CHOLESTEROL': {'high': 200},
            'TOTAL_CLAIMS_COST': {'high': 10000},
            'IN_ADM': {'high': 2},
            'OUT_VISITS': {'high': 10},
            'ED_VISITS': {'high': 2},
            'RX_ADH': {'low': 0.8}
        }

    def extract_features(self, top_features: str) -> List[str]:
        """Extract feature names from the top features string"""
        if not top_features or top_features == 'N/A':
            return []
        
        # Split by comma and clean up feature names
        features = [f.strip() for f in top_features.split(',')]
        return features

    def get_feature_value(self, patient_data: Dict, feature: str) -> float:
        """Get the value of a specific feature from patient data"""
        feature_mapping = {
            'AGE': 'AGE',
            'BMI': 'BMI',
            'BP_S': 'BP_S',
            'GLUCOSE': 'GLUCOSE',
            'HbA1c': 'HbA1c',
            'CHOLESTEROL': 'CHOLESTEROL',
            'TOTAL_CLAIMS_COST': 'TOTAL_CLAIMS_COST',
            'IN_ADM': 'IN_ADM',
            'OUT_VISITS': 'OUT_VISITS',
            'ED_VISITS': 'ED_VISITS',
            'RX_ADH': 'RX_ADH'
        }
        
        data_key = feature_mapping.get(feature)
        if data_key and data_key in patient_data:
            try:
                return float(patient_data[data_key])
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    def get_risk_level(self, feature: str, value: float) -> str:
        """Determine risk level for a feature based on its value"""
        thresholds = self.risk_thresholds.get(feature, {})
        
        if feature == 'AGE':
            if value >= thresholds.get('high_risk', 75):
                return 'high_risk'
            elif value >= thresholds.get('moderate_risk', 65):
                return 'moderate_risk'
        elif feature in ['BMI', 'BP_S', 'GLUCOSE', 'HbA1c', 'CHOLESTEROL', 'TOTAL_CLAIMS_COST', 'IN_ADM', 'OUT_VISITS', 'ED_VISITS']:
            if value >= thresholds.get('high', float('inf')):
                return 'high'
        elif feature == 'RX_ADH':
            if value <= thresholds.get('low', 0):
                return 'low'
        
        return 'normal'

    def generate_recommendations(self, patient_data: Dict, top_features: str) -> List[str]:
        """Generate personalized intervention recommendations"""
        recommendations = []
        seen_recommendations = set()
        
        # Extract top features
        features = self.extract_features(top_features)
        
        # Add recommendations based on top features
        for feature in features:
            if feature in self.intervention_map:
                interventions = self.intervention_map[feature]
                
                if isinstance(interventions, dict):
                    # Feature with risk-level specific interventions
                    value = self.get_feature_value(patient_data, feature)
                    risk_level = self.get_risk_level(feature, value)
                    
                    if risk_level in interventions:
                        for intervention in interventions[risk_level]:
                            if intervention not in seen_recommendations:
                                recommendations.append(intervention)
                                seen_recommendations.add(intervention)
                else:
                    # Feature with direct interventions
                    for intervention in interventions:
                        if intervention not in seen_recommendations:
                            recommendations.append(intervention)
                            seen_recommendations.add(intervention)
        
        # Add risk-level based general recommendations
        risk_30d = patient_data.get('RISK_30D', 0)
        if risk_30d >= 80:
            general_recommendations = [
                "Immediate care coordination recommended",
                "Consider intensive case management",
                "Schedule urgent follow-up appointment"
            ]
        elif risk_30d >= 60:
            general_recommendations = [
                "Enhanced care monitoring recommended",
                "Schedule follow-up within 2 weeks",
                "Implement preventive care strategies"
            ]
        elif risk_30d >= 40:
            general_recommendations = [
                "Regular monitoring recommended",
                "Annual wellness visit scheduling",
                "Preventive care optimization"
            ]
        else:
            general_recommendations = [
                "Continue preventive care routine",
                "Annual wellness visit recommended",
                "Maintain healthy lifestyle practices"
            ]
        
        # Add general recommendations
        for rec in general_recommendations:
            if rec not in seen_recommendations and len(recommendations) < 3:
                recommendations.append(rec)
                seen_recommendations.add(rec)
        
        # Limit to 3 recommendations
        return recommendations[:3]

    def format_recommendations(self, recommendations: List[str]) -> str:
        """Format recommendations for display"""
        if not recommendations:
            return "Continue current care plan"
        
        formatted = []
        for i, rec in enumerate(recommendations, 1):
            formatted.append(f"{i}. {rec}")
        
        return " | ".join(formatted)

# Global recommender instance
recommender = InterventionRecommender()

def get_ai_recommendations(patient_data: Dict, top_features: str) -> str:
    """Get AI recommendations for a patient"""
    recommendations = recommender.generate_recommendations(patient_data, top_features)
    return recommender.format_recommendations(recommendations)
