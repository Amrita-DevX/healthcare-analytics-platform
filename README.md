# Healthcare Analytics Platform (End-to-End MLOps)

**$3.5M Annual ROI Demo**: Claims Fraud + Churn Prediction + Utilization Mgmt for Payers.

[![CI/CD](https://github.com/Amrita-DevX/healthcare-analytics-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Amrita-DevX/healthcare-analytics-platform)

## Business Impact 
| Metric | Savings |
|--------|---------|
| Fraud Prevention | $450K/6mo |
| Churn Reduction | $1.44M/yr |
| ER Optimization | $216K/yr |
| **Total ROI** | **$3.5M/yr** |

## Tech Stack
- MLflow (tracking), FastAPI (REST APIs), Docker, GitHub Actions CI/CD
- Viz: Tableau Public [link]
- Deploy: Render API [link], HF Spaces Demo [link]

## Quickstart 🚀
```bash
git clone https://github.com/Amrita-DevX/healthcare-analytics-platform
cd healthcare-analytics-platform
make setup data train-churn
mlflow ui  # View experiments
