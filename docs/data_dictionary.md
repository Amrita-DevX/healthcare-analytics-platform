# CMS DE-SynPUF Data Dictionary

## Overview
This data dictionary describes the CMS DE-SynPUF (Synthetic Medicare Claims) datasets used for fraud detection and healthcare analytics.

**Data Source:** Centers for Medicare & Medicaid Services (CMS)  
**Dataset:** DE-SynPUF Sample 1  
**Years:** 2008-2010  
**Beneficiaries:** ~116,000 synthetic Medicare beneficiaries  

---

## 📋 Beneficiary Summary Files
*Files: DE1_0_2008/2009/2010_Beneficiary_Summary_File_Sample_1.csv*

### Demographics & Identifiers

| Column | Type | Description | Values/Range | Notes |
|--------|------|-------------|--------------|-------|
| `DESYNPUF_ID` | String | Unique beneficiary ID | e.g., "00013D2EFD8E45D1" | Links to claims |
| `BENE_BIRTH_DT` | Integer | Birth date | YYYYMMDD format | Age can be calculated |
| `BENE_DEATH_DT` | Float | Death date | YYYYMMDD or NaN | NaN = still alive |
| `BENE_SEX_IDENT_CD` | Integer | Gender | 1=Male, 2=Female | - |
| `BENE_RACE_CD` | Integer | Race | 1=White, 2=Black, 3=Other, 5=Hispanic | CMS coding |
| `BENE_ESRD_IND` | String | End-Stage Renal Disease | "Y"=Yes, "0"=No | High-cost condition |

### Geographic Information

| Column | Type | Description | Values/Range | Notes |
|--------|------|-------------|--------------|-------|
| `SP_STATE_CODE` | Integer | State code | 1-54 | FIPS state codes |
| `BENE_COUNTY_CD` | Integer | County code | 0-999 | Within state |

### Coverage Information

| Column | Type | Description | Values/Range | Notes |
|--------|------|-------------|--------------|-------|
| `BENE_HI_CVRAGE_TOT_MONS` | Integer | Hospital Insurance months | 0-12 | Medicare Part A |
| `BENE_SMI_CVRAGE_TOT_MONS` | Integer | Supplementary Medical Insurance months | 0-12 | Medicare Part B |
| `BENE_HMO_CVRAGE_TOT_MONS` | Integer | HMO coverage months | 0-12 | Medicare Advantage |
| `PLAN_CVRG_MOS_NUM` | Integer | Part D coverage months | 0-12 | Prescription drugs |

### Chronic Conditions (Binary Flags)

| Column | Description | Values |
|--------|-------------|--------|
| `SP_ALZHDMTA` | Alzheimer's Disease or Related Dementia | 1=Yes, 2=No |
| `SP_CHF` | Congestive Heart Failure | 1=Yes, 2=No |
| `SP_CHRNKIDN` | Chronic Kidney Disease | 1=Yes, 2=No |
| `SP_CNCR` | Cancer | 1=Yes, 2=No |
| `SP_COPD` | Chronic Obstructive Pulmonary Disease | 1=Yes, 2=No |
| `SP_DEPRESSN` | Depression | 1=Yes, 2=No |
| `SP_DIABETES` | Diabetes | 1=Yes, 2=No |
| `SP_ISCHMCHT` | Ischemic Heart Disease | 1=Yes, 2=No |
| `SP_OSTEOPRS` | Osteoporosis | 1=Yes, 2=No |
| `SP_RA_OA` | Rheumatoid Arthritis / Osteoarthritis | 1=Yes, 2=No |
| `SP_STRKETIA` | Stroke / Transient Ischemic Attack | 1=Yes, 2=No |

### Annual Costs by Service Type

**Inpatient (IP):**
| Column | Description | Notes |
|--------|-------------|-------|
| `MEDREIMB_IP` | Medicare reimbursement for inpatient | Amount paid by Medicare |
| `BENRES_IP` | Beneficiary responsibility for inpatient | Deductibles + coinsurance |
| `PPPYMT_IP` | Primary payer payment for inpatient | Other insurance |

**Outpatient (OP):**
| Column | Description | Notes |
|--------|-------------|-------|
| `MEDREIMB_OP` | Medicare reimbursement for outpatient | - |
| `BENRES_OP` | Beneficiary responsibility for outpatient | - |
| `PPPYMT_OP` | Primary payer payment for outpatient | - |

**Carrier (CAR) - Physician Services:**
| Column | Description | Notes |
|--------|-------------|-------|
| `MEDREIMB_CAR` | Medicare reimbursement for carrier | - |
| `BENRES_CAR` | Beneficiary responsibility for carrier | - |
| `PPPYMT_CAR` | Primary payer payment for carrier | - |

---

## 🏥 Inpatient Claims
*File: DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv*

### Claim Identifiers

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `DESYNPUF_ID` | String | Beneficiary ID | Links to beneficiary file |
| `CLM_ID` | Integer | Unique claim ID | Primary key |
| `SEGMENT` | Integer | Claim line segment | Multiple lines per claim |
| `CLM_FROM_DT` | Float | Claim start date | YYYYMMDD format |
| `CLM_THRU_DT` | Float | Claim end date | YYYYMMDD format |
| `PRVDR_NUM` | String | Provider ID | Hospital identifier |

### Payment Information

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `CLM_PMT_AMT` | Float | Claim payment amount | Total Medicare payment |
| `NCH_PRMRY_PYR_CLM_PD_AMT` | Float | Primary payer amount | Other insurance |
| `NCH_BENE_IP_DDCTBL_AMT` | Float | Beneficiary deductible | Out-of-pocket cost |
| `NCH_BENE_PTA_COINSRNC_LBLTY_AM` | Float | Coinsurance liability | 20% after deductible |
| `NCH_BENE_BLOOD_DDCTBL_LBLTY_AM` | Float | Blood deductible | Rare |
| `CLM_PASS_THRU_PER_DIEM_AMT` | Float | Pass-through per diem | Special payments |

### Physician Information

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `AT_PHYSN_NPI` | Float | Attending physician NPI | Primary doctor |
| `OP_PHYSN_NPI` | Float | Operating physician NPI | Surgeon |
| `OT_PHYSN_NPI` | Float | Other physician NPI | Additional provider |

### Clinical Information

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `CLM_ADMSN_DT` | Integer | Admission date | YYYYMMDD |
| `NCH_BENE_DSCHRG_DT` | Integer | Discharge date | YYYYMMDD |
| `CLM_UTLZTN_DAY_CNT` | Float | Length of stay | Days |
| `ADMTNG_ICD9_DGNS_CD` | Integer | Admitting diagnosis | ICD-9 code |
| `CLM_DRG_CD` | Integer | Diagnosis Related Group | Payment category |

### Diagnosis Codes (ICD-9)

| Column | Description | Notes |
|--------|-------------|-------|
| `ICD9_DGNS_CD_1` | Primary diagnosis | Most important |
| `ICD9_DGNS_CD_2` to `ICD9_DGNS_CD_10` | Secondary diagnoses | Additional conditions |

### Procedure Codes (ICD-9)

| Column | Description | Notes |
|--------|-------------|-------|
| `ICD9_PRCDR_CD_1` to `ICD9_PRCDR_CD_6` | Procedure codes | Surgeries/treatments |

### HCPCS Codes (Healthcare Common Procedure Coding System)

| Column | Description | Notes |
|--------|-------------|-------|
| `HCPCS_CD_1` to `HCPCS_CD_45` | Service/supply codes | DME, drugs, services |

---

## 🏢 Outpatient Claims
*File: DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv*

### Claim Identifiers
Same as inpatient: `DESYNPUF_ID`, `CLM_ID`, `SEGMENT`, `CLM_FROM_DT`, `CLM_THRU_DT`, `PRVDR_NUM`

### Payment Information

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `CLM_PMT_AMT` | Float | Claim payment amount | Medicare payment |
| `NCH_PRMRY_PYR_CLM_PD_AMT` | Float | Primary payer amount | - |
| `NCH_BENE_PTB_DDCTBL_AMT` | Float | Part B deductible | Annual deductible |
| `NCH_BENE_PTB_COINSRNC_AMT` | Float | Part B coinsurance | 20% typically |
| `NCH_BENE_BLOOD_DDCTBL_LBLTY_AM` | Float | Blood deductible | - |

### Physician Information
Same as inpatient: `AT_PHYSN_NPI`, `OP_PHYSN_NPI`, `OT_PHYSN_NPI`

### Clinical Information

| Column | Description | Notes |
|--------|-------------|-------|
| `ADMTNG_ICD9_DGNS_CD` | Admitting diagnosis | - |
| `ICD9_DGNS_CD_1` to `ICD9_DGNS_CD_10` | Diagnosis codes | - |
| `ICD9_PRCDR_CD_1` to `ICD9_PRCDR_CD_6` | Procedure codes | - |
| `HCPCS_CD_1` to `HCPCS_CD_45` | Service codes | - |

---

## 🔍 Key Features for Fraud Detection

### High-Risk Indicators

1. **Payment Anomalies:**
   - Unusually high `CLM_PMT_AMT` for diagnosis
   - Mismatched diagnosis-procedure combinations
   - Zero or negative payments

2. **Provider Patterns:**
   - High claim volume per provider
   - Provider specialization mismatch
   - Geographic clustering

3. **Beneficiary Patterns:**
   - Excessive utilization
   - Multiple providers for same condition
   - Service dates inconsistencies

4. **Clinical Flags:**
   - Diagnosis codes without supporting procedures
   - Conflicting diagnoses
   - Unusual length of stay

---

## 📊 Data Quality Notes

**Missing Values:**
- HCPCS codes: ~60-90% missing (not all claims require)
- Death dates: Missing = beneficiary alive
- Some diagnosis/procedure codes: Legitimately empty

**Data Types:**
- Dates stored as integers (YYYYMMDD format)
- Some columns mixed types (need conversion)
- NaN vs 0 distinction important for flags

**Known Issues:**
- BENE_ESRD_IND: Mixed type (String "Y" or Integer 0)
- Some procedure codes stored as strings vs floats
- Segment numbers indicate claim line items (need aggregation)

---

## 🎯 Feature Engineering Opportunities

1. **Aggregate features:** Claims per beneficiary, total annual costs
2. **Time-based:** Days between claims, seasonality
3. **Clinical:** Chronic condition count, comorbidity index
4. **Provider:** Claims volume, specialization patterns
5. **Geographic:** State/county risk scores
6. **Diagnosis diversity:** Number of unique diagnoses
7. **Cost ratios:** Medicare reimbursement / beneficiary responsibility

---

## 📚 References

- [CMS DE-SynPUF Documentation](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs)
- [ICD-9 Code Reference](https://www.icd9data.com/)
- [HCPCS Code Reference](https://www.cms.gov/medicare/coding-billing/hcpcsreleasecodesets)
- [Medicare Claims Processing Manual](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Internet-Only-Manuals-IOMs)