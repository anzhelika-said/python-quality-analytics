# Manufacturing Quality Analytics — Python Portfolio Project

## Project overview
This project demonstrates an end-to-end Python data analysis workflow using a **fully synthetic manufacturing quality dataset**. It explores inspection volumes, defect rates, supplier patterns, defect categories and production downtime.

The scenario is fictional and the dataset contains no employer, customer or personal information.

## Business questions
1. How many units were inspected and how many defects were recorded?
2. How does the overall defect rate change month by month?
3. Which suppliers have the highest observed defect rates?
4. Which defect categories occur most often?
5. How is downtime distributed across production lines?

## Tools
- Python
- pandas
- matplotlib
- Jupyter Notebook (optional)

## Repository structure
```text
python-quality-analytics/
├── data/
│   └── raw/
│       └── synthetic_quality_data.csv
├── notebooks/
│   └── 01_quality_analysis.ipynb
├── src/
│   └── analysis.py
├── outputs/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/python-quality-analytics.git
cd python-quality-analytics
```

### 2. Create and activate a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the analysis
```bash
python src/analysis.py
```

The script validates the input data, calculates summary metrics and saves CSV summaries plus a monthly trend chart in `outputs/`.

### 5. Explore the notebook
```bash
jupyter notebook
```
Open `notebooks/01_quality_analysis.ipynb`.

## Data dictionary

| Column | Description |
|---|---|
| `inspection_date` | Date of the inspection record |
| `product_family` | Fictional product category |
| `supplier` | Fictional supplier label |
| `production_line` | Production line identifier |
| `shift` | Inspection shift |
| `units_inspected` | Number of units inspected |
| `defect_units` | Number of defective units |
| `defect_category` | Recorded defect type |
| `severity` | Defect severity label |
| `downtime_minutes` | Production downtime associated with the record, in minutes |

Each row represents one fictional inspection batch/record. `defect_units` is a count within `units_inspected`; the overall defect rate is calculated as total defective units divided by total inspected units.

## Key analytical decisions
- The overall defect rate is calculated using total counts, not by taking a simple average of row-level percentages.
- Supplier comparisons should be interpreted with the inspection volume in mind.
- The dataset is synthetic and designed for portfolio demonstration, not operational decision-making.

## Next improvements
- Add confidence intervals or statistical tests for supplier comparisons.
- Add a Power BI dashboard using the same dataset.
- Add automated data-quality checks and a reusable reporting export.

## Disclaimer
All data and supplier/product names in this repository are fictional and generated for demonstration purposes. No confidential employer or client data is included.
