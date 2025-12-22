"""
Fraud Detection Dashboard - Streamlit Web Application

This interactive dashboard demonstrates the Medicare fraud detection system.
Allows users to input claim details and get real-time fraud predictions with explanations.

To run:
    streamlit run fraud_detection_app.py

Features:
- Real-time fraud prediction
- Risk tier classification
- Top risk factors display
- Model performance metrics
- Interactive visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Get project root (healthcare-analytics-platform/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Add parent directory to path to import models
sys.path.append(str(Path(__file__).parent.parent.parent))

# Page configuration
st.set_page_config(
    page_title="Medicare Fraud Detection",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .risk-high {
        background-color: #ff4444;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .risk-medium {
        background-color: #ffaa00;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .risk-low {
        background-color: #00cc66;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load model and preprocessing objects
@st.cache_resource
def load_model():
    """Load trained model and preprocessing objects"""
    try:
        model = joblib.load(PROJECT_ROOT/'models'/'fraud'/'xgboost_model.pkl')
        feature_list = joblib.load(PROJECT_ROOT/'models'/'fraud'/'feature_list.pkl')
        return model, feature_list
    except FileNotFoundError:
        st.error("Model files not found. Please ensure models are trained.")
        return None, None

model, feature_list = load_model()

# Helper functions
def get_risk_tier(probability):
    """Classify risk based on probability"""
    if probability >= 0.7:
        return "CRITICAL", "risk-high"
    elif probability >= 0.5:
        return "HIGH", "risk-high"
    elif probability >= 0.3:
        return "MEDIUM", "risk-medium"
    else:
        return "LOW", "risk-low"

def get_recommendation(probability):
    """Get action recommendation"""
    if probability >= 0.6:
        return "🚨 MANUAL REVIEW REQUIRED - High fraud indicators detected"
    elif probability >= 0.4:
        return "⚠️ ELEVATED REVIEW - Additional scrutiny recommended"
    else:
        return "✅ AUTO-APPROVE - No significant fraud indicators"

def create_gauge_chart(probability):
    """Create gauge chart for fraud probability"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Fraud Probability", 'font': {'size': 24}},
        delta = {'reference': 50, 'increasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#90EE90'},
                {'range': [30, 50], 'color': '#FFD700'},
                {'range': [50, 70], 'color': '#FFA500'},
                {'range': [70, 100], 'color': '#FF6347'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        font={'size': 16}
    )
    
    return fig

# App header
st.markdown('<p class="main-header">🏥 Medicare Fraud Detection System</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Model Information
with st.sidebar:
    st.header("📊 Model Information")
    st.info("""
    **Model:** XGBoost Classifier
    
    **Performance:**
    - ROC-AUC: 99.9%
    - Recall: 95.7%
    - Precision: 57.9%
    
    **Decision Threshold:** 0.60
    
    **Trained on:** 117K Medicare claims
    """)
    
    st.markdown("---")
    
    st.header("🎯 Risk Tiers")
    st.markdown("""
    **CRITICAL** (≥70%): Immediate investigation
    
    **HIGH** (50-70%): Manual review required
    
    **MEDIUM** (30-50%): Elevated scrutiny
    
    **LOW** (<30%): Auto-approve
    """)
    
    st.markdown("---")
    
    st.header("📈 System Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fraud Detected", "95.7%", "↑ High recall")
    with col2:
        st.metric("False Alarms", "0.24%", "↓ Low FP rate")

# Main content tabs
tab1, tab2, tab3 = st.tabs(["🔍 Claim Analysis", "📊 Model Performance", "💡 About"])

# TAB 1: Claim Analysis
with tab1:
    st.header("Enter Claim Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Claim Information")
        claim_amount = st.number_input(
            "Claim Amount ($)", 
            min_value=0.0, 
            max_value=100000.0, 
            value=15000.0,
            step=100.0
        )
        
        length_of_stay = st.number_input(
            "Length of Stay (days)", 
            min_value=0, 
            max_value=90, 
            value=3
        )
        
        diagnosis_count = st.slider(
            "Number of Diagnoses", 
            min_value=1, 
            max_value=10, 
            value=3
        )
        
        procedure_count = st.slider(
            "Number of Procedures", 
            min_value=0, 
            max_value=6, 
            value=2
        )
    
    with col2:
        st.subheader("Provider Information")
        provider_claim_count = st.number_input(
            "Provider Total Claims", 
            min_value=1, 
            max_value=1000, 
            value=150
        )
        
        provider_avg_payment = st.number_input(
            "Provider Avg Payment ($)", 
            min_value=0.0, 
            max_value=50000.0, 
            value=12000.0,
            step=100.0
        )
        
        provider_payment_cv = st.slider(
            "Provider Payment Variance", 
            min_value=0.0, 
            max_value=2.0, 
            value=0.5,
            step=0.1,
            help="Coefficient of variation (std/mean)"
        )
    
    with col3:
        st.subheader("Beneficiary Information")
        bene_age = st.slider(
            "Patient Age", 
            min_value=18, 
            max_value=100, 
            value=70
        )
        
        chronic_conditions = st.slider(
            "Chronic Conditions", 
            min_value=0, 
            max_value=11, 
            value=2
        )
        
        bene_claim_count = st.number_input(
            "Patient Total Claims", 
            min_value=1, 
            max_value=500, 
            value=20
        )
        
        bene_unique_providers = st.number_input(
            "Unique Providers Seen", 
            min_value=1, 
            max_value=50, 
            value=3
        )
    
    # Analyze button
    st.markdown("---")
    
    if st.button("🔍 Analyze Claim", type="primary", use_container_width=True):
        if model is None:
            st.error("Model not loaded. Cannot make predictions.")
        else:
            # Calculate derived features
            payment_per_day = claim_amount / max(length_of_stay, 1)
            payment_deviation = claim_amount - provider_avg_payment
            cost_per_condition = claim_amount / max(chronic_conditions, 1)
            
            # Calculate z-score (simplified)
            payment_zscore = (claim_amount - 10000) / 5000
            
            # Create feature vector (simplified - using subset of features)
            # In production, you'd need all 40 features
            features_dict = {
                'CLM_PMT_AMT': claim_amount,
                'length_of_stay': length_of_stay,
                'payment_per_day': payment_per_day,
                'diagnosis_code_count': diagnosis_count,
                'procedure_code_count': procedure_count,
                'provider_claim_count': provider_claim_count,
                'provider_avg_payment': provider_avg_payment,
                'provider_payment_cv': provider_payment_cv,
                'bene_claim_count': bene_claim_count,
                'bene_unique_providers': bene_unique_providers,
                'age': bene_age,
                'chronic_condition_count': chronic_conditions,
                'payment_zscore': payment_zscore,
                'payment_deviation_from_provider_avg': payment_deviation,
                'cost_per_condition': cost_per_condition
            }
            
            # Fill missing features with defaults
            feature_vector = []
            for feat in feature_list:
                if feat in features_dict:
                    feature_vector.append(features_dict[feat])
                else:
                    feature_vector.append(0)  # Default value
            
            X = np.array([feature_vector])
            
            # Make prediction
            fraud_probability = model.predict_proba(X)[0][1]
            fraud_prediction = model.predict(X)[0]
            
            # Display results
            st.markdown("---")
            st.header("📋 Analysis Results")
            
            # Results layout
            result_col1, result_col2, result_col3 = st.columns([2, 2, 3])
            
            with result_col1:
                st.plotly_chart(create_gauge_chart(fraud_probability), use_container_width=True)
            
            with result_col2:
                st.markdown("### Classification")
                risk_tier, risk_class = get_risk_tier(fraud_probability)
                st.markdown(f'<div class="{risk_class}">{risk_tier} RISK</div>', unsafe_allow_html=True)
                
                st.markdown("### Recommendation")
                recommendation = get_recommendation(fraud_probability)
                st.info(recommendation)
            
            with result_col3:
                st.markdown("### Top Risk Factors")
                
                # Get feature importance from model
                feature_importance = model.feature_importances_
                top_features_idx = np.argsort(feature_importance)[-5:][::-1]
                
                risk_factors = []
                for idx in top_features_idx:
                    if idx < len(feature_list):
                        feat_name = feature_list[idx]
                        feat_value = feature_vector[idx]
                        importance = feature_importance[idx]
                        risk_factors.append({
                            'Factor': feat_name,
                            'Value': f"{feat_value:.2f}",
                            'Importance': f"{importance:.3f}"
                        })
                
                risk_df = pd.DataFrame(risk_factors)
                st.dataframe(risk_df, hide_index=True, use_container_width=True)
            
            # Detailed breakdown
            st.markdown("---")
            st.subheader("📊 Detailed Analysis")
            
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.markdown("**Claim Characteristics**")
                st.write(f"- Claim Amount: ${claim_amount:,.2f}")
                st.write(f"- Payment per Day: ${payment_per_day:,.2f}")
                st.write(f"- Z-Score: {payment_zscore:.2f}")
                st.write(f"- Deviation from Provider Avg: ${payment_deviation:,.2f}")
                
                st.markdown("**Clinical Complexity**")
                st.write(f"- Diagnoses: {diagnosis_count}")
                st.write(f"- Procedures: {procedure_count}")
                st.write(f"- Chronic Conditions: {chronic_conditions}")
                st.write(f"- Cost per Condition: ${cost_per_condition:,.2f}")
            
            with detail_col2:
                st.markdown("**Provider Profile**")
                st.write(f"- Total Claims: {provider_claim_count}")
                st.write(f"- Average Payment: ${provider_avg_payment:,.2f}")
                st.write(f"- Payment Variability: {provider_payment_cv:.2f}")
                
                st.markdown("**Beneficiary Profile**")
                st.write(f"- Age: {bene_age}")
                st.write(f"- Total Claims: {bene_claim_count}")
                st.write(f"- Unique Providers: {bene_unique_providers}")
                st.write(f"- Provider Shopping Ratio: {bene_unique_providers/max(bene_claim_count, 1):.3f}")

# TAB 2: Model Performance
with tab2:
    st.header("Model Performance Metrics")
    
    # Display comparison chart
    st.subheader("Model Comparison: Logistic Regression vs XGBoost")
    try:
        from PIL import Image
        comparison_img = Image.open(PROJECT_ROOT/'docs'/'model_comparison_comprehensive.png')
        st.image(comparison_img, use_container_width=True)
    except:
        st.info("Comparison chart not found. Run model comparison notebook first.")
    
    st.markdown("---")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="ROC-AUC",
            value="99.9%",
            delta="+0.1% vs baseline",
            help="Area under ROC curve - measures discrimination ability"
        )
    
    with col2:
        st.metric(
            label="Precision",
            value="57.9%",
            delta="+73.7% vs baseline",
            help="Of flagged claims, % that are actually fraud"
        )
    
    with col3:
        st.metric(
            label="Recall",
            value="95.7%",
            delta="Same as baseline",
            help="Of actual fraud, % that we catch"
        )
    
    with col4:
        st.metric(
            label="F1-Score",
            value="72.1%",
            delta="+45.9% vs baseline",
            help="Harmonic mean of precision and recall"
        )
    
    st.markdown("---")
    
    # Business impact
    st.subheader("Business Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Cost Savings**")
        st.write("- False Positives: 32 (vs 88 baseline)")
        st.write("- Review Cost Reduction: $1,960")
        st.write("- 64% fewer false alarms")
        
        st.markdown("**Fraud Detection**")
        st.write("- Fraud Caught: 44 out of 46")
        st.write("- Detection Rate: 95.7%")
        st.write("- Fraud Prevented: $670K")
    
    with col2:
        st.markdown("**ROI Analysis**")
        st.write("- Net Benefit: $669K per 13K claims")
        st.write("- ROI: 59,748%")
        st.write("- Projected Annual Savings: $176M (for 500K claims)")
        
        st.markdown("**Operational Efficiency**")
        st.write("- Review top 10% → Catch 58% fraud")
        st.write("- Review top 20% → Catch 78% fraud")
        st.write("- Dramatically improves analyst efficiency")

# TAB 3: About
with tab3:
    st.header("About This System")
    
    st.markdown("""
    ## Medicare Fraud Detection System
    
    This system uses advanced machine learning to detect fraudulent Medicare claims 
    with high accuracy while minimizing false positives.
    
    ### Key Features
    
    - **99.9% AUC Performance:** Near-perfect discrimination between fraud and legitimate claims
    - **95.7% Recall:** Catches 44 out of 46 fraud cases in test set
    - **57.9% Precision:** Nearly 6 out of 10 flagged claims are actually fraudulent
    - **Real-time Scoring:** Instant fraud risk assessment for incoming claims
    - **Explainable AI:** SHAP values explain why claims are flagged
    
    ### Technical Approach
    
    **Data Sources:**
    - CMS DE-SynPUF (Synthetic Medicare Claims)
    - 117,000 inpatient claims (2008-2010)
    - 116,000 beneficiaries
    
    **Feature Engineering:**
    - 50+ features across provider, beneficiary, and claim characteristics
    - Statistical outlier detection (z-scores, percentiles)
    - Behavioral patterns (utilization, provider shopping)
    - Clinical complexity indicators
    
    **Modeling:**
    - Baseline: Logistic Regression (interpretable, fast)
    - Production: XGBoost (higher precision, fewer false positives)
    - SMOTE for class imbalance (4% fraud rate)
    - Hyperparameter tuning with 5-fold cross-validation
    
    **Explainability:**
    - SHAP (SHapley Additive exPlanations)
    - Waterfall plots for individual predictions
    - Feature importance rankings
    - Regulatory compliance ready
    
    ### Business Impact
    
    **For Healthcare Payers:**
    - Reduce fraud losses by catching 95%+ of fraudulent claims
    - Lower operational costs with 64% fewer false positives
    - Improve provider satisfaction with more accurate flagging
    - Projected $176M annual savings for mid-size payer (500K claims/year)
    
    **For Fraud Analysts:**
    - Prioritized investigation queue (high-risk first)
    - Clear explanations for each flagged claim
    - Efficient resource allocation
    - Review top 20% of claims to catch 78% of fraud
    
    ### Deployment
    
    This dashboard demonstrates the fraud detection system capabilities.
    Production deployment includes:
    - REST API for real-time scoring
    - Batch processing for nightly claim reviews
    - Integration with claims management systems
    - Automated alerting for critical cases
    - Monthly model retraining with new confirmed fraud
    
    ### Development
    
    Developed as part of a comprehensive healthcare analytics platform portfolio project.
    
    **Author:** Technology Analyst | Healthcare Data Analytics
    
    **Technologies:** Python, XGBoost, SHAP, Streamlit, scikit-learn
    
    **GitHub:** [Healthcare Analytics Platform](https://github.com/Amrita-DevX/healthcare-analytics-platform)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 1rem;'>
    <p>Medicare Fraud Detection System v1.0</p>
    <p>Built with Streamlit | Powered by XGBoost</p>
</div>
""", unsafe_allow_html=True)