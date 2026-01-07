"""
make_dataset.py - Data Loading Pipeline

What this does:
    1. Reads config.yaml to get all settings
    2. Loads raw CMS files (beneficiaries, claims, prescriptions)
    3. Combines them into unified tables
    4. Saves to data/interim/ folder
    5. Logs everything to MLflow

Why config.yaml is used here:
    - Get paths from config instead of hardcoding
    - Get file format (parquet vs csv) from config
    - Get MLflow settings from config
    - Everything configurable without changing code
"""

import pandas as pd
from pathlib import Path
import logging
import mlflow
import yaml
import sys

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """
    Load settings from config.yaml file.
    
    Why this function exists:
        We need to read the YAML file and convert it to a Python dictionary.
        This dictionary is then passed to all other functions.
    
    Args:
        config_path: Path to config.yaml file (e.g., "configs/config.yaml")
    
    Returns:
        Dictionary with all settings
    
    Example:
        config = load_config("configs/config.yaml")
        print(config['data']['raw_path'])  # Prints: data/raw
    """
    
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Loaded configuration from {config_path}")
    return config


def load_beneficiaries(raw_path: Path) -> pd.DataFrame:
    """
    Load beneficiary files from 3 years and combine them.
    
    Args:
        raw_path: Directory containing raw CSV files
    
    Returns:
        DataFrame with unique members (latest year data)
    """
    
    logger.info("Loading beneficiary files...")
    
    # CORRECTED file names to match YOUR actual files
    files = [
        'Beneficiary_2008.csv',
        'Beneficiary_2009.csv',
        'Beneficiary_2010.csv'
    ]
    
    dfs = []
    
    for filename in files:
        filepath = raw_path / filename
        
        if filepath.exists():
            df = pd.read_csv(filepath, dtype={'DESYNPUF_ID': str}, low_memory=False)
            dfs.append(df)
            logger.info(f"  Loaded {filename}: {len(df):,} rows")
        else:
            logger.warning(f"  File not found: {filename}")
    
    if not dfs:
        raise ValueError("No beneficiary files were loaded")
    
    combined = pd.concat(dfs, ignore_index=True)
    logger.info(f"  Combined: {len(combined):,} total rows")
    
    unique = combined.drop_duplicates(subset='DESYNPUF_ID', keep='last')
    logger.info(f"  Unique members: {len(unique):,}")
    
    return unique


def load_claims(raw_path: Path, claim_type: str) -> pd.DataFrame:
    """
    Load inpatient or outpatient claims files.
    
    Args:
        raw_path: Directory containing raw CSV files
        claim_type: Either "Inpatient" or "Outpatient"
    
    Returns:
        DataFrame with all claims
    """
    
    logger.info(f"Loading {claim_type} claims...")
    
    # CORRECTED: Your files are named Inpatient_Claims.csv and Outpatient_Claims.csv
    # Use exact filename instead of glob pattern
    filename = f"{claim_type}_Claims.csv"
    filepath = raw_path / filename
    
    if not filepath.exists():
        logger.warning(f"  File not found: {filename}")
        return pd.DataFrame()
    
    df = pd.read_csv(filepath, dtype={'DESYNPUF_ID': str, 'CLM_ID': str}, low_memory=False)
    logger.info(f"  Loaded {filename}: {len(df):,} rows")
    
    return df



def load_prescriptions(raw_path: Path) -> pd.DataFrame:
    """
    Load prescription drug files.
    
    Why we do this:
        - Prescriptions are medication dispensing events
        - Optional data (pipeline continues if not found)
    
    Args:
        raw_path: Directory containing raw CSV files
    
    Returns:
        DataFrame with all prescriptions (or empty DataFrame if not found)
    """
    
    logger.info("Loading prescription files...")
    
    pattern = "*Prescription*.csv"
    files = list(raw_path.glob(pattern))
    
    if not files:
        logger.warning("  No prescription files found")
        return pd.DataFrame()
    
    dfs = []
    
    for filepath in files:
        df = pd.read_csv(filepath, dtype={'DESYNPUF_ID': str}, low_memory=False)
        dfs.append(df)
        logger.info(f"  Loaded {filepath.name}: {len(df):,} rows")
    
    combined = pd.concat(dfs, ignore_index=True)
    logger.info(f"  Total prescriptions: {len(combined):,}")
    
    return combined


def save_data(data: dict, output_path: Path, config: dict) -> None:
    """
    Save all DataFrames to files.
    
    Why config is used here:
        - config tells us: save as parquet or csv?
        - config tells us: use compression or not?
        - No hardcoding - all flexible
    
    Args:
        data: Dictionary containing DataFrames (beneficiaries, claims, etc.)
        output_path: Directory to save files
        config: Settings from config.yaml
    """
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get settings from config
    output_format = config['data_loading']['output_format']
    compression = config['data_loading']['compression']
    
    logger.info(f"Saving data to {output_path} (format: {output_format}, compression: {compression})")
    
    # Define what to save
    files_to_save = {
        'beneficiaries': 'beneficiaries',
        'inpatient': 'inpatient_claims',
        'outpatient': 'outpatient_claims',
        'prescriptions': 'prescriptions'
    }
    
    for key, filename in files_to_save.items():
        df = data.get(key)
        
        if df is not None and not df.empty:
            # Build filename based on config (e.g., beneficiaries.parquet)
            output_file = output_path / f"{filename}.{output_format}"
            
            # Save based on format from config
            if output_format == 'parquet':
                df.to_parquet(output_file, index=False, compression=compression)
            elif output_format == 'csv':
                df.to_csv(output_file, index=False)
            else:
                raise ValueError(f"Unsupported format: {output_format}")
            
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            logger.info(f"  Saved {output_file.name}: {file_size_mb:.2f} MB")


def run_pipeline(config: dict) -> dict:
    """
    Main function that runs the entire data loading pipeline.
    
    Why config is passed here:
        - All settings come from config.yaml
        - Paths, MLflow settings, file formats - all from config
        - Makes pipeline flexible and configurable
    
    Args:
        config: Dictionary loaded from config.yaml
    
    Returns:
        Dictionary containing all loaded DataFrames
    """
    
    # Get paths from config (not hardcoded!)
    project_root = Path(__file__).resolve().parents[2]
    raw_path = project_root / config['data']['raw_path']
    interim_path = project_root / config['data']['interim_path']
    
    logger.info("=" * 70)
    logger.info(f"Starting {config['project']['name']} Data Loading Pipeline")
    logger.info(f"Version: {config['project']['version']}")
    logger.info(f"Raw data: {raw_path}")
    logger.info(f"Output: {interim_path}")
    logger.info("=" * 70)
    
    # Setup MLflow from config
    mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
    mlflow.set_experiment(config['mlflow']['experiment_name'])
    
    # Start MLflow run to track this execution
    with mlflow.start_run(run_name="data_loading_pipeline"):
        
        # Load all data
        beneficiaries = load_beneficiaries(raw_path)
        inpatient = load_claims(raw_path, 'Inpatient')
        outpatient = load_claims(raw_path, 'Outpatient')
        prescriptions = load_prescriptions(raw_path)
        
        # Package data
        data = {
            'beneficiaries': beneficiaries,
            'inpatient': inpatient,
            'outpatient': outpatient,
            'prescriptions': prescriptions
        }
        
        # Log data stats to MLflow
        mlflow.log_param("total_beneficiaries", len(beneficiaries))
        mlflow.log_param("inpatient_claims", len(inpatient))
        mlflow.log_param("outpatient_claims", len(outpatient))
        mlflow.log_param("prescription_records", len(prescriptions))
        
        # Log config settings to MLflow (so we know what settings were used)
        mlflow.log_param("output_format", config['data_loading']['output_format'])
        mlflow.log_param("compression", config['data_loading']['compression'])
        
        # Quality check from config
        min_rows = config['data_loading']['min_rows']
        if len(beneficiaries) < min_rows:
            raise ValueError(f"Only {len(beneficiaries)} beneficiaries loaded, minimum is {min_rows}")
        
        # Save data
        save_data(data, interim_path, config)
        
        logger.info("Pipeline completed successfully")
        
        return data


if __name__ == '__main__':
    """
    This runs when you execute: python src/data/make_dataset.py
    """
    
    try:
        # Step 1: Load config.yaml
        config = load_config('configs/config.yaml')
        
        # Step 2: Run pipeline with config
        data = run_pipeline(config)
        
        # Step 3: Print summary
        print("\n" + "=" * 70)
        print("DATA LOADING COMPLETE")
        print("=" * 70)
        print(f"Beneficiaries:       {len(data['beneficiaries']):>10,} records")
        print(f"Inpatient Claims:    {len(data['inpatient']):>10,} records")
        print(f"Outpatient Claims:   {len(data['outpatient']):>10,} records")
        print(f"Prescriptions:       {len(data['prescriptions']):>10,} records")
        print("=" * 70)
        print(f"Saved to: data/interim/")
        print(f"MLflow UI: {config['mlflow']['tracking_uri']}")
        print("=" * 70)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)
