# 🎯 TalentSight — Employee Attrition Intelligence Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talentsight-employee-attrition-intelligence-platform-fr89qx8kn.streamlit.app/)

> *An end-to-end HR analytics platform that predicts employee flight risk, segments the workforce into actionable retention personas, and quantifies the financial impact of attrition — built to demonstrate production-grade data science for MNC hiring panels.*

---

## 🔗 Live Demo

**[→ Open TalentSight App](https://talentsight-employee-attrition-intelligence-platform-fr89qx8kn.streamlit.app/)**

---

## 📌 Business Problem

A mid-size IT services firm is losing employees at 16.1% annually — 2.3× the industry benchmark. At an estimated replacement cost of 1.5× annual salary per employee, this represents a **$20.4M annual liability**.

TalentSight identifies flight-risk employees 45–60 days before they resign, surfaces the drivers of attrition by segment, and quantifies the financial return of targeted retention interventions.

**Key result:** Optimising the classification threshold from 0.50 to 0.29 saves **$881,686 annually** by catching 13 additional leavers at the cost of 32 additional retention conversations.

---

## 🏗️ Project Architecture

```
Data Sources → Collection → Audit → Cleaning → EDA →
Feature Engineering → Modelling → Clustering → Deployment
```

### Data Sources (4 sources)
| Source | Type | Records | Purpose |
|---|---|---|---|
| IBM HR Analytics Dataset | CSV (Kaggle) | 1,470 employees | Primary modelling dataset |
| Bureau of Labor Statistics | REST API | 84 rows | National labour market benchmarks |
| Synthetic Payroll | Generated (Faker) | 35,286 rows | 24-month compensation history |
| IBM Glassdoor Reviews | Web Scraped | — | External sentiment benchmarking |

---

## 📊 Results

### XGBoost Attrition Classifier
| Metric | Value |
|---|---|
| Test AUC-ROC | 0.817 |
| Cross-Validation AUC (5-fold) | 0.831 |
| Optimal Threshold | 0.29 |
| Annual Cost Saving vs Default | $881,686 |

### K-Means Workforce Segmentation (K=5)
| Segment | Size | Attrition Rate | Risk |
|---|---|---|---|
| Overworked Juniors | 305 | **36.72%** | 🔴 Critical |
| Disengaged Juniors | 737 | 12.48% | 🟡 Medium |
| Stagnant Mid-Seniors | 136 | 11.76% | 🟡 Medium |
| Senior Stable | 162 | 6.17% | 🟢 Low |
| High Potential Fast Trackers | 130 | **5.38%** | 🟢 Lowest |

---

## 🔑 Key Features

### Novel Feature Engineering
- **`overtime_month_ratio`** — 24-month overtime frequency (ranked #1 by SHAP, outperforming every IBM raw feature)
- **`career_stagnation_index`** — YearsAtCompany / (NumCompaniesWorked + 1)
- **`promotion_velocity`** — YearsAtCompany / (YearsSinceLastPromotion + 1)
- **`salary_growth_rate`** — 24-month salary trajectory vs IBM point-in-time snapshot
- **`avg_bonus_pct`** — compensation quality relative to base pay

### Business Cost Threshold Optimisation
Rather than maximising F1, the classification threshold is tuned to minimise **total business cost** — replacement cost ($117K) vs intervention cost ($20K). This is the approach consultants at Deloitte and McKinsey actually use.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Data Collection | Python, Requests, BeautifulSoup, BLS API, Faker |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost, SHAP |
| Database | PostgreSQL, SQLAlchemy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Deployment | Streamlit Community Cloud |
| BI Dashboard | Power BI Desktop |
| Version Control | Git, GitHub |

---

## 📁 Repository Structure

```
talentsight/
├── data/
│   ├── raw/                    # IBM CSV, BLS JSON
│   ├── processed/              # Cleaned and feature-engineered datasets
│   └── scraped/                # Web scraped data
├── notebooks/
│   ├── 01_Data_Audit.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_Data_Collection.ipynb
│   ├── 05_Feature_Engineering.ipynb
│   ├── 06_Model_Training_And_Evaluation.ipynb
│   └── 07_KMeans_Clustering.ipynb
├── sql_analysis/
│   ├── 01_attrition_overview.sql
│   ├── 02_flight_risk_cte.sql
│   ├── 03_income_percentiles.sql
│   └── 04_attrition_trend.sql
├── app/
│   └── main.py                 # Streamlit application
├── models/
│   ├── xgb_pipeline.pkl
│   ├── kmeans_model.pkl
│   └── optimal_threshold.pkl
├── powerbi/
│   └── talentsight_dashboard.pbix
└── report/
    └── talentsight_report.pdf
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- PostgreSQL 14+
- Power BI Desktop

### Installation

```bash
# Clone the repository
git clone https://github.com/Saheri-Adak/TalentSight-Employee-Attrition-Intelligence-Platform.git
cd TalentSight-Employee-Attrition-Intelligence-Platform/talentsight

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file in the `talentsight/` directory:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=talentsight
DB_USER=postgres
DB_PASSWORD=your_password
BLS_API_KEY=your_bls_api_key
```

### Run the Streamlit App Locally
```bash
streamlit run app/main.py
```

### Load Data into PostgreSQL
```bash
python sql_analysis/load_data.py
```

---

## 📓 Notebooks Overview

| Notebook | Description |
|---|---|
| `01_Data_Audit` | Data quality profiling — shape, nulls, duplicates, distributions |
| `02_Data_Cleaning` | Drop constants, encode target, cast ordinals |
| `03_EDA` | Business-framed insights across 3 dimensions: who, why, cost |
| `04_Data_Collection` | BLS API, synthetic payroll generation, web scraping |
| `05_Feature_Engineering` | Multi-source merge, domain feature creation, ColumnTransformer |
| `06_Model_Training` | LR baseline, XGBoost tuning, SHAP analysis, cost threshold optimisation |
| `07_KMeans_Clustering` | Workforce segmentation, elbow + silhouette, cluster validation |

---

## 🔍 SQL Analysis Layer

Four SQL files demonstrate analysis deliverable without Python:

- **`01_attrition_overview.sql`** — Attrition rates by department, job level, segment
- **`02_flight_risk_cte.sql`** — Rule-based flight risk scoring using CTEs
- **`03_income_percentiles.sql`** — Salary benchmarking with window functions
- **`04_attrition_trend.sql`** — LAG() and running totals on BLS and payroll data

---

## 💡 Key Analytical Findings

1. **Overtime is the strongest attrition predictor** — `overtime_month_ratio` ranked #1 by SHAP (0.864 mean absolute value), outperforming every IBM raw feature including MonthlyIncome and Age

2. **1 in 3 Overworked Juniors leave** — employees working overtime 73% of months at Job Level 1 leave at 36.72% — 7× the rate of High Potential Fast Trackers

3. **No stock options = 24.4% attrition** — employees with zero equity stake leave at nearly 3× the rate of those with any stock options

4. **The first 2 years are critical** — 28.9% of New Joiners leave within 2 years; loyalty stabilises sharply after 5 years

5. **BusinessTravel shows Simpson's Paradox** — frequent travelers appear lower risk after controlling for job role and income, contradicting the raw EDA finding

6. **Optimal threshold saves $881K** — tuning from 0.50 to 0.29 catches 13 additional leavers at the cost of 32 extra retention conversations

---

## 👩‍💻 Author

**Saheri Adak**
- 🔗 GitHub: [@Saheri-Adak](https://github.com/Saheri-Adak)
- 💼 LinkedIn: [linkedin.com/in/saheri-adak-99290030a](https://linkedin.com/in/saheri-adak-99290030a)
- 📊 Kaggle: [kaggle.com/saheriadak](https://kaggle.com/saheriadak)

---

## 📄 License

This project is licensed under the MIT License.

---

*Built as a portfolio project targeting Data Analyst and Data Science internship roles at MNCs, consulting firms, and product companies.*
