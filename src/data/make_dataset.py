"""
CMS DE-SynPUF Data Processing Pipeline
Purpose: Transform raw CMS files into ML-ready datasets
Input: data/raw/Beneficiary_*.csv, Inpatient_Claims.csv, Outpatient_Claims.csv
Output: data/processed/member_churn.parquet (ready for XGBoost)
Why: YAML config externalizes parameters for easy changes across environments
"""

import pandas as pd
from pathlib import Path
import yaml
import logging

# Setup logging to track pipeline execution
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """
    Load configuration from YAML file
    
    Why YAML config:
    - Separates code from parameters (change settings without editing code)
    - Easy to version control different environments (dev/test/prod)
    - Standard in enterprise ML (MLOps best practice)
    - Business stakeholders can adjust params without coding
    """
    with open('configs/config.yaml', 'r') as f:
        return yaml.safe_load(f)

def load_beneficiary_data(raw_path):
    """
    Load beneficiary demographic files from 2008, 2009, 2010
    
    Why this function exists:
    - Beneficiary data contains member demographics and chronic conditions
    - These are key predictors of churn (age, sex, disease burden)
    - We combine 3 years to get complete member history
    
    Your columns used:
    - DESYNPUF_ID: Unique member identifier
    - BENE_SEX_IDENT_CD: Gender (1=male, 2=female)
    - BENE_RACE_CD: Race code
    - SP_ALZHDMTA, SP_CHF, SP_CNCR: Chronic condition flags
    """
    file_mapping = {
        'Beneficiary_2008.csv': 2008,
        'Beneficiary_2009.csv': 2009,
        'Beneficiary_2010.csv': 2010
    }
    
    df_list = []
    for filename, year in file_mapping.items():
        file_path = raw_path / filename
        if file_path.exists():
            # dtype={'DESYNPUF_ID': str} prevents ID corruption
            # low_memory=False handles large CMS files efficiently
            df = pd.read_csv(file_path, dtype={'DESYNPUF_ID': str}, low_memory=False)
            df['YEAR'] = year
            df_list.append(df)
            logger.info(f"Loaded {filename}: {df.shape}")
    
    # Combine all years and deduplicate
    beneficiaries = pd.concat(df_list, ignore_index=True)
    unique_beneficiaries = beneficiaries.drop_duplicates('DESYNPUF_ID')
    logger.info(f"Beneficiaries: {unique_beneficiaries.shape}")
    return unique_beneficiaries

def load_claims_data(raw_path):
    """
    Load inpatient and outpatient claims
    
    Why this function exists:
    - Claims show utilization patterns (predict churn)
    - High utilization = dissatisfaction risk
    - Low utilization = disengagement risk
    
    Your columns used:
    - CLM_ID: Claim count (utilization measure)
    - CLM_PMT_AMT: Spend amount
    - ICD9_DGNS_CD_1: Diagnosis variety
    """
    inpatient_file = raw_path / 'Inpatient_Claims.csv'
    outpatient_file = raw_path / 'Outpatient_Claims.csv'
    
    claims_dfs = []
    
    if inpatient_file.exists():
        df = pd.read_csv(inpatient_file, dtype={'DESYNPUF_ID': str}, low_memory=False)
        df['claim_type'] = 'inpatient'
        claims_dfs.append(df)
        logger.info(f"Inpatient: {df.shape}")
    
    if outpatient_file.exists():
        df = pd.read_csv(outpatient_file, dtype={'DESYNPUF_ID': str}, low_memory=False)
        df['claim_type'] = 'outpatient'
        claims_dfs.append(df)
        logger.info(f"Outpatient: {df.shape}")
    
    if claims_dfs:
        return pd.concat(claims_dfs, ignore_index=True)
    return pd.DataFrame()

def engineer_features(beneficiaries, claims, config):
    """
    Create ML features from raw data
    
    Why feature engineering:
    - Aggregates claim-level to member-level (many rows → one row per member)
    - Creates business features (high_util_risk from config threshold)
    - Binary encoding for ML (female, chronic_count)
    
    Uses config for:
    - high_utilizer_percentile: Define "high utilizer" threshold (80th percentile)
    """
    
    if claims.empty:
        claims_agg = pd.DataFrame({'DESYNPUF_ID': beneficiaries['DESYNPUF_ID']})
    else:
        # Aggregate claims per member
        claims_agg = claims.groupby('DESYNPUF_ID').agg({
            'CLM_ID': 'count',                          # Total claims
            'CLM_PMT_AMT': 'sum',                       # Total spend
            'ICD9_DGNS_CD_1': lambda x: x.astype(str).nunique()  # DX variety
        }).round(2)
        
        claims_agg.columns = ['total_claims', 'total_spend', 'dx_variety']
        
        # Use config threshold (not hardcoded 0.8)
        util_threshold = config['data']['high_utilizer_percentile']
        claims_agg['high_util_risk'] = (claims_agg['total_claims'] > 
                                       claims_agg['total_claims'].quantile(util_threshold)).astype(int)
        claims_agg = claims_agg.reset_index()
    
    # Demographics
    demo_features = beneficiaries[['DESYNPUF_ID', 'BENE_SEX_IDENT_CD', 'BENE_RACE_CD',
                                  'SP_ALZHDMTA', 'SP_CHF', 'SP_CNCR']].copy()
    
    demo_features['female'] = (demo_features['BENE_SEX_IDENT_CD'] == 2).astype(int)
    demo_features['chronic_count'] = demo_features[['SP_ALZHDMTA', 'SP_CHF', 'SP_CNCR']].sum(axis=1)
    
    # Merge
    final_features = demo_features.merge(claims_agg, on='DESYNPUF_ID', how='left').fillna(0)
    logger.info(f"Features: {final_features.shape}")
    return final_features

def main():
    """
    Main pipeline with time-based churn definition
    Churn = Members active in 2008-2009 but NOT in 2010
    """
    config = load_config()
    
    raw_path = Path('data/raw')
    processed_path = Path('data/processed')
    processed_path.mkdir(exist_ok=True)
    
    beneficiaries = load_beneficiary_data(raw_path)
    claims = load_claims_data(raw_path)
    
    feature_df = engineer_features(beneficiaries, claims, config)
    feature_df.to_parquet(processed_path / 'member_features.parquet', index=False)
    
    # Better churn definition: Active 2008-2009 but missing in 2010
    # Read beneficiary files to check 2010 presence
    bene_2010 = pd.read_csv(raw_path / 'Beneficiary_2010.csv', dtype={'DESYNPUF_ID': str}, usecols=['DESYNPUF_ID'])
    active_2010_ids = set(bene_2010['DESYNPUF_ID'])
    
    # Churn = 1 if member NOT in 2010 file
    feature_df['churn'] = (~feature_df['DESYNPUF_ID'].isin(active_2010_ids)).astype(int)
    
    ml_dataset = feature_df[['DESYNPUF_ID', 'churn', 'chronic_count', 'female',
                           'total_claims', 'total_spend', 'high_util_risk', 'dx_variety']].copy()
    ml_dataset.to_parquet(processed_path / 'member_churn.parquet', index=False)
    
    churn_rate = ml_dataset['churn'].mean()
    cost_per_member = config['business']['churn_cost_per_member']
    revenue_risk = churn_rate * len(ml_dataset) * cost_per_member
    
    print(f"\nSUCCESS:")
    print(f"Shape: {ml_dataset.shape}")
    print(f"Churn Rate: {churn_rate:.1%}")
    print(f"Revenue Risk: ${revenue_risk:,.0f}")
    print(f"Churned Members: {ml_dataset['churn'].sum():,}")


if __name__ == "__main__":
    main()
