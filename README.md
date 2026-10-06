# Customer Segmentation & Churn Pattern Analytics — European Banking

A segmentation-driven analysis of customer churn across 10,000 retail banking customers in France, Germany, and Spain — built with **Python** (EDA), **Power BI** (dashboard design), and deployed live via **Streamlit**, with a full research paper and stakeholder executive summary.

### 🔗 [**Live Dashboard →**](https://hyufmh7prwujuw92h8szej.streamlit.app)

> **TL;DR:** Overall churn is 20.37%, but that number hides a lot. Germany churns at double the rate of its peers, the 46–60 age group is the single highest-risk segment, and — counter-intuitively — the bank's *highest-balance* customers churn *more*, not less. Churned high-value customers alone represent **€185.6M** in balances, with German customers aged 30–45 accounting for 27% of that risk on their own.

---

## 📌 Project Overview

Banks track churn as a single aggregate rate, which tells them customers are leaving but not *which* customers, *why*, or *what it's costing them*. This project builds a segmentation framework — by geography, age, gender, tenure, credit score, and account balance — to turn that single number into an actionable risk map, then quantifies the financial exposure it represents.

**Prepared for:** Unified Mentor | Subject: The European Central Bank
**Author:** Taha S. Travadi — GEC Bhavnagar, Computer Engineering

---

## 🎯 Objectives

**Primary**
- Measure the overall churn rate
- Identify how churn is distributed across customer segments
- Compare churn behaviour across geographies

**Secondary**
- Quantify churn specifically among high-value customers
- Evaluate the relationship between tenure/engagement and churn
- Deliver a live, interactive tool for ongoing retention decision-making

---

## 🗂️ Dataset

10,000 customer records, 14 original fields (one — `Year` — was a constant and dropped during cleaning).

| Column | Description |
|---|---|
| `CustomerId` | Unique customer identifier |
| `CreditScore` | Creditworthiness (350–850) |
| `Geography` | France, Germany, or Spain |
| `Gender` | Male / Female |
| `Age` | Customer age |
| `Tenure` | Years with the bank |
| `Balance` | Account balance |
| `NumOfProducts` | Number of bank products held |
| `HasCrCard` | Credit card ownership (binary) |
| `IsActiveMember` | Activity indicator (binary) |
| `EstimatedSalary` | Estimated annual salary |
| `Exited` | **Target** — churn indicator (1 = churned) |

Four segmentation fields were engineered for analysis: `AgeGroup`, `CreditBand`, `TenureGroup`, `BalanceSegment`.

---

## 🛠️ Tools & Stack

| Purpose | Tool |
|---|---|
| Data cleaning & EDA | Python (pandas, matplotlib, seaborn) |
| Dashboard design | Power BI Desktop (DAX measures, synced slicers, drill-down) |
| Live deployment | Python + Streamlit (deployed via Streamlit Community Cloud) |
| Reporting | Word / PDF (research paper + executive summary) |

---

## 📊 Key Findings

| Metric | Value |
|---|---|
| Overall churn rate | **20.37%** |
| Highest-risk geography | **Germany — 32.44%** (vs. ~16% France/Spain) |
| Highest-risk age group (by rate) | **46–60 — 51.12%** |
| Highest-volume age group (by count) | **30–45** (5,921 customers; 45.7% of high-value churners) |
| Gender gap | Female **25.07%** vs. Male **16.46%** |
| Tenure effect | Negligible (19.67%–21.15% across all tenure groups) |
| High-value churn rate | **25.23%** |
| Revenue at risk | **€185.59M** (29.21% of all high-value balances) |
| Sharpest concentration | **Germany + age 30–45** = 27% of all high-value churners |

**The core counter-intuitive finding:** high-balance customers churn *more* than low/zero-balance customers — the bank's most financially valuable customers are also its highest flight risk.

---

## 📈 Dashboard

The dashboard covers 4 core modules, each with live filters (Geography, Gender, Age Group, Balance Segment):

1. **Overall Churn Summary** — headline KPIs, retained vs. churned split, churn by gender
2. **Geography-wise Churn Visualization** — heatmap of churn by geography × age group, geography × gender matrix
3. **Age & Tenure Churn Comparison** — churn rate by age/tenure, combo chart (count + rate) showing the rate-vs-volume distinction
4. **High-Value Customer Churn Explorer** — high-value KPIs, age-vs-balance scatter, geography × age high-value churn matrix

**Two versions are included in this repo:**

| Version | Purpose | Link |
|---|---|---|
| 🟢 **Streamlit (live, public)** | Deployed web app — no login required | [**Open live app**](https://hyufmh7prwujuw92h8szej.streamlit.app) |
| 🔵 **Power BI (`.pbix`)** | Original design with DAX measures, synced slicers, and drill-down hierarchy | `dashboard/Churn_Dashboard.pbix` (open in Power BI Desktop) |

> **Why two versions?** The dashboard was originally built in Power BI. When publishing it as a public web link turned out to be disabled at the organization/admin level, the same analysis was re-implemented in Python + Streamlit so it could be shared as a live, publicly accessible link with zero setup for the viewer.

See `/dashboard/screenshots/` for Power BI page previews.

---

## 📁 Repository Structure

```
├── app.py                                        # Streamlit app (live dashboard source)
├── requirements.txt                              # Streamlit app dependencies
├── bank_churn_cleaned.csv                        # Cleaned + segmented dataset (used by app.py)
├── data/
│   └── European_Bank.csv                         # Raw dataset
├── notebooks/
│   └── Churn_analysis.ipynb                      # Python EDA notebook
├── dashboard/
│   └── Churn_Dashboard.pbix                      # Power BI dashboard (original design)
│   └── screenshots/                              # Power BI page exports
├── reports/
│   └── Churn_Analytics_Research_Paper.pdf        # Full research paper
│   └── Churn_Analytics_Executive_Summary.pdf     # 1-page stakeholder summary
└── README.md
```

> **Note:** `app.py`, `requirements.txt`, and `bank_churn_cleaned.csv` must stay in the repo **root** (not inside a subfolder) for the Streamlit deployment to find them correctly.

---

## 🚀 How to Explore This Project

1. **Read the findings fast:** start with `reports/Churn_Analytics_Executive_Summary.pdf` (1 page)
2. **Go deep:** `reports/Churn_Analytics_Research_Paper.pdf` has full methodology, EDA, and recommendations
3. **Explore interactively (live, no install needed):** open the **[Streamlit app](https://hyufmh7prwujuw92h8szej.streamlit.app)** — all filters update in real time
4. **See the original dashboard design:** open `dashboard/Churn_Dashboard.pbix` in [Power BI Desktop](https://powerbi.microsoft.com/desktop/) to explore the DAX measures and drill-down hierarchy
5. **See the code:** `notebooks/Churn_analysis.ipynb` has the full Python cleaning + EDA pipeline, and `app.py` has the Streamlit app source

---

## 💡 Recommendations (Summary)

- Prioritize retention spend in **Germany**, especially customers aged 30–60 with high balances
- Build proactive outreach for high-balance customers aged **46–60** before inactivity signals appear
- Investigate the **gender churn gap** qualitatively (surveys/exit interviews), especially in Germany
- Reduce reliance on tenure-based loyalty programs — tenure shows no real protective effect
- Use the dashboard as a **live monitoring tool** for relationship managers and regional leadership, not a one-time report

---

## 🔭 Future Work

- Multi-year data to analyze churn trends over time
- Incorporate qualitative churn-cause data (complaints, exit reasons)
- Build a predictive model (logistic regression / gradient boosting) for individual customer risk scoring
- Composite high-value definition combining balance, salary, and product holdings

---

## 📄 License

This project is for educational and portfolio purposes.
