# Member Experience KPI Dashboard

End-to-end analytics dashboard tracking healthcare member experience metrics — satisfaction scores, call center performance, digital engagement, and operational KPIs across regions and time periods.

## Business Problem

Healthcare organizations need real-time visibility into member experience to reduce churn, improve HEDIS/CAHPS scores, and meet regulatory reporting requirements. This project builds a comprehensive KPI framework from raw operational data.

## Key Metrics Tracked

| KPI Category | Metrics |
|-------------|---------|
| **Member Satisfaction** | NPS, CSAT, Satisfaction Trend |
| **Call Center** | Avg Handle Time, First Contact Resolution, Abandonment Rate |
| **Digital Engagement** | Portal Login Rate, Mobile App Adoption, Online Claim Submissions |
| **Operational** | Claims Processing Time, Prior Auth Turnaround, Grievance Resolution |
| **Retention** | Disenrollment Rate, Voluntary Churn, Win-back Rate |

## Approach

1. **Synthetic Data Generation** — 12 months of member experience data across 5 regions with realistic seasonality and variance
2. **KPI Computation Engine** — Modular functions to compute each metric from raw data with configurable time windows
3. **Trend Analysis** — Month-over-month and rolling averages to detect performance shifts
4. **Regional Benchmarking** — Compare KPIs across regions to identify best practices and intervention areas
5. **Interactive Visualizations** — Plotly-based charts for drill-down exploration plus static matplotlib summaries

## Tech Stack

- **Python** — pandas, numpy
- **Visualization** — matplotlib, seaborn, plotly
- **Notebook** — Jupyter for interactive exploration
- **Data** — Synthetic healthcare member data

## Project Structure

```
├── README.md
├── requirements.txt
├── data/
│   └── member_experience_data.csv
├── src/
│   ├── generate_data.py
│   ├── kpi_engine.py
│   └── visualizations.py
└── notebooks/
    └── kpi_dashboard.ipynb
```

## How to Run

```bash
pip install -r requirements.txt
python src/generate_data.py
jupyter notebook notebooks/kpi_dashboard.ipynb
```

## Skills Demonstrated

- Healthcare domain KPI design (HEDIS/CAHPS alignment)
- Dashboard development and data storytelling
- Time-series trend analysis
- Regional benchmarking and variance analysis
- Python data engineering and visualization
