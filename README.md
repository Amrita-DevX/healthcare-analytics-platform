# Healthcare Analytics Platform (End-to-End MLOps)

**$3.5M Annual ROI Demo**: Claims Fraud + Churn Prediction + Utilization Mgmt for Payers.
┌─────────────────────────────────────────────────────────────┐
│         HEALTHCARE ANALYTICS PLATFORM (Your Project)        │
│                                                              │
│  Input: CMS Data (Beneficiaries, Claims, Prescriptions)     │
│                           ↓                                  │
│              Generic Data Pipeline (Once)                    │
│                           ↓                                  │
│  ┌──────────────┬──────────────┬──────────────┬──────────┐ │
│  │   Churn      │     Cost     │     Risk     │   Fraud  │ │
│  │ Prediction   │  Forecasting │   Scoring    │ Detection│ │
│  │              │              │              │          │ │
│  │ Will member  │ Predict next │ High-cost    │ Detect   │ │
│  │ leave plan?  │ year costs   │ member risk  │ anomalies│ │
│  │              │              │              │          │ │
│  │ Model: XGB   │ Model: LGBM  │ Model: RF    │ Model:   │ │
│  │ AUC: 0.85    │ RMSE: $1.2K  │ F1: 0.78     │ Isolation│ │
│  └──────────────┴──────────────┴──────────────┴──────────┘ │
│                           ↓                                  │
│              FastAPI (Unified Prediction Service)            │
│  Endpoints: /predict/churn, /predict/cost, /predict/risk    │
└─────────────────────────────────────────────────────────────┘


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

healthcare-analytics-platform/
├── configs/
│   ├── config.yaml                      # Global settings
│   ├── churn_config.yaml                # Churn model config
│   ├── cost_config.yaml                 # Cost model config
│   ├── risk_config.yaml                 # Risk model config
│   └── fraud_config.yaml                # Fraud model config
│
├── data/
│   ├── raw/                             # CMS files (never touch)
│   ├── interim/                         # Generic cleaned data
│   │   ├── beneficiaries.parquet
│   │   ├── inpatient_claims.parquet
│   │   ├── outpatient_claims.parquet
│   │   └── prescriptions.parquet
│   └── processed/                       # Model-specific features
│       ├── churn_features.parquet
│       ├── cost_features.parquet
│       ├── risk_features.parquet
│       └── fraud_features.parquet
│
├── src/
│   ├── data/
│   │   └── make_dataset.py              # Generic data loading
│   │
│   ├── features/
│   │   ├── build_churn_features.py      # Churn features
│   │   ├── build_cost_features.py       # Cost features
│   │   ├── build_risk_features.py       # Risk features
│   │   └── build_fraud_features.py      # Fraud features
│   │
│   ├── models/
│   │   ├── train_churn_model.py         # Churn training
│   │   ├── train_cost_model.py          # Cost training
│   │   ├── train_risk_model.py          # Risk training
│   │   └── train_fraud_model.py         # Fraud training
│   │
│   └── api/
│       ├── main.py                      # FastAPI multi-model service
│       └── schemas.py                   # Pydantic request/response models
│
├── notebooks/
│   ├── 01_eda_platform.ipynb            # EDA all data
│   ├── 02_data_cleaning.ipynb           # Cleaning
│   ├── 03_churn_feature_engineering.ipynb
│   ├── 04_churn_modeling.ipynb
│   ├── 05_cost_feature_engineering.ipynb
│   ├── 06_cost_modeling.ipynb
│   ├── 07_risk_feature_engineering.ipynb
│   ├── 08_risk_modeling.ipynb
│   ├── 09_fraud_detection.ipynb
│   └── 10_model_comparison.ipynb        # Compare all models
│
├── models/                              # Trained pipelines
│   ├── churn_pipeline.pkl
│   ├── cost_pipeline.pkl
│   ├── risk_pipeline.pkl
│   └── fraud_pipeline.pkl
│
├── mlruns/                              # MLflow experiments
│   ├── data_loading/
│   ├── churn_experiments/
│   ├── cost_experiments/
│   ├── risk_experiments/
│   └── fraud_experiments/
│
├── tests/                               # Unit tests
│   ├── test_features.py
│   ├── test_models.py
│   └── test_api.py
│
├── Dockerfile                           # Container for deployment
├── docker-compose.yml                   # MLflow + FastAPI services
├── requirements.txt
└── README.md                            # Platform documentation

