# Healthcare Analytics Platform
**End-to-End ML System for Healthcare Payer Optimization**

## 🎯 Project Overview
Integrated machine learning platform addressing four critical healthcare payer challenges:
1. **Fraud Detection & Claims Auto-Adjudication** - Automated claims processing with fraud prevention
2. **Member Churn Prediction** - Proactive retention interventions
3. **Healthcare Utilization Analysis** - Optimize care setting and reduce costs
4. **Care Gap Closure** - Predictive preventive care outreach

## 💰 Business Impact (Projected)
- **$3.5M+ annual ROI** for mid-size payer (50K-100K members)
- **$1.8M** in claims processing cost savings
- **$450K** fraud prevention in 6 months
- **12%** member retention improvement
- **18%** reduction in avoidable ER visits

## 🛠️ Tech Stack
**ML/Data Science:** Python, scikit-learn, XGBoost, TensorFlow, pandas, numpy  
**Deployment:** AWS SageMaker / Lambda, Streamlit Cloud  
**Visualization:** Plotly, Streamlit, Power BI  
**MLOps:** MLflow, DVC, GitHub Actions  
**Database:** PostgreSQL, SQLite  

## 📊 Data Sources

**Primary Dataset: CMS DE-SynPUF (Synthetic Medicare Claims)**
- Beneficiary Summary Files: 2008, 2009, 2010
- Inpatient Claims: 2008-2010
- Outpatient Claims: 2008-2010
- Source: Centers for Medicare & Medicaid Services
- Size: ~100,000 beneficiaries, ~500K+ claims
- [CMS Data Link](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs)

This synthetic dataset mimics real Medicare claims structure while protecting patient privacy.

## 📊 Modules

### 1. Fraud Detection & Auto-Adjudication
*Status: 🚧 In Progress*
- Hybrid ML system combining supervised and unsupervised learning
- Real-time claim scoring API
- Graph analytics for provider collusion detection

### 2. Member Churn Prediction
*Status: 📋 Planned*
- Ensemble models (XGBoost + Survival Analysis)
- Uplift modeling for intervention optimization
- Personalized retention strategies

### 3. Utilization Analysis
*Status: 📋 Planned*
- Anomaly detection for over/under-utilization
- Setting-of-care optimization
- Prescriptive analytics for cost reduction

### 4. Care Gap Prediction
*Status: 📋 Planned*
- Multi-label classification for preventive care gaps
- HEDIS measure optimization
- Proactive outreach prioritization

## 🚀 Quick Start
```bash
# Clone repository
git clone https://github.com/Amrita-DevX/healthcare-analytics-platform

# Setup environment
conda create -n healthcare-ml python=3.10
conda activate healthcare-ml
pip install -r requirements.txt

# Run notebooks
jupyter lab
```

## 📈 Model Performance
*Coming soon - metrics will be updated as modules are completed*

## 📝 Documentation
Detailed documentation for each module can be found in the `/docs` folder.

## 👨‍💻 Author
**Amrita Das**  
Technology Analyst | Healthcare Data Analytics  
[LinkedIn](https://www.linkedin.com/in/amrita-dasdev/) | [Email](amritarimu@gmail.com)

---
*This is a portfolio project demonstrating end-to-end ML capabilities for healthcare analytics.*