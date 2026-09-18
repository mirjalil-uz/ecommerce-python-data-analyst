# E-Commerce Sales & Customer Analysis with Python

## Project Overview
This intermediate-level data analytics project analyzes e-commerce transaction data to understand sales performance, profitability, customer value, product categories, and regional trends.

The project demonstrates an end-to-end analyst workflow using Python: data cleaning, exploratory analysis, feature engineering, KPI calculation, visualization, and business recommendations.

## Business Questions
- How do revenue and profit change over time?
- Which product categories generate the most revenue and profit?
- Which regions contribute the most profit?
- Which customers generate the highest revenue?
- How do discounts relate to profitability?
- What products may require pricing or margin review?

## Tools & Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Dataset
The dataset contains 15,000+ e-commerce transactions across:
- 2024-01-01 to 2025-06-30
- 3,000 customers
- 4 U.S. regions
- 5 product categories
- Consumer, Corporate, and Small Business segments

The dataset intentionally includes a small number of missing values and duplicate records so the project demonstrates realistic data-cleaning work.

## Analysis Workflow
1. Load and inspect the data
2. Identify missing values and duplicates
3. Clean and standardize fields
4. Create derived metrics such as profit margin and monthly period
5. Calculate business KPIs
6. Analyze sales and profit trends
7. Compare categories and regions
8. Analyze customer value
9. Visualize findings
10. Translate findings into business recommendations

## Key Skills Demonstrated
- Data cleaning and validation
- Exploratory Data Analysis (EDA)
- Aggregation and groupby analysis
- Feature engineering
- KPI development
- Customer segmentation analysis
- Time-series analysis
- Data visualization
- Business-oriented interpretation

## Running This Project (VS Code)

1. Open the project folder in VS Code.
2. Create and activate a virtual environment, then install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # on Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. In VS Code, select `.venv` as the Python interpreter (Command Palette → "Python: Select Interpreter").
4. Run either artifact — both cover the same analysis:
   - **Notebook (recommended, matches the write-up above):** open `notebooks/ecommerce_sales_analysis.ipynb` and Run All.
   - **Script:** open `src/data_analysis.py` and click Run, or `python src/data_analysis.py` from a terminal at the project root. It prints the KPI/analysis tables to the console and saves charts to `images/`.

Both entry points resolve the data path relative to their own file location, so it doesn't matter which folder your terminal/VS Code happens to be in when you run them.

## Repository Structure
```text
ecommerce-python-data-analyst/
├── data/
│   └── ecommerce_sales.csv
├── notebooks/
│   └── ecommerce_sales_analysis.ipynb
├── src/
│   └── data_analysis.py
├── images/
├── README.md
├── requirements.txt
└── .gitignore
```

## Business Deliverable
The final notebook is designed to communicate findings to a non-technical stakeholder, not just display Python code. Each analysis section should explain what the metric means, what the chart shows, and why the finding matters to the business.

## Author
Mirjalil Mirfozilov
