##  Data Setup

**Note:** Raw data files are excluded from this repository due to size (>400MB total).

### Download Instructions:

1. Visit [CMS DE-SynPUF Sample 1](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF)
2. Download these 5 files:
   - `DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv`
   - `DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv`
   - `DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv`
   - `DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv`
   - `DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv`
3. Place all files in `data/raw/cms_synpuf/` folder
4. Run `notebooks/00_data_verification.ipynb` to verify setup

### Quick Start:
```bash
# Clone repository
git clone https://github.com/Amrita-DevX/healthcare-analytics-platform.git

# Setup Python environment
conda create -n healthcare-ml python=3.10
conda activate healthcare-ml
pip install -r requirements.txt

# Download data (see instructions above)

# Run notebooks
jupyter lab
```