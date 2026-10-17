# Superstore Sales Analytics

End-to-end analysis of retail sales data (2014-2017) to find what drives profit and where the business loses money. The pipeline goes from a raw Excel file through Python (Pandas) cleaning and EDA, a MySQL database with SQL business queries, and a Power BI dashboard.

![Dashboard overview](images/dashboard_overview.png)

## Business problem

A retail sales manager wants to know which categories, regions and discount levels make money, and which ones lose it. This project answers that with Python, SQL and Power BI.

## Tools

Python (Pandas, Matplotlib, SQLAlchemy) · MySQL · SQL (CTEs, window functions) · Power BI · DAX

## Dataset

Sample Superstore: 9,994 rows (order lines), 5,009 unique orders, 1,850 products, orders from 2014-01-03 to 2017-12-30. No missing values or duplicate rows were found in cleaning. Money values are shown as in the source file, without a currency symbol.

## Workflow

```
data/raw/superstore_raw.xlsx
   -> scripts/clean_data.py       standardise column names, trim text, parse dates and numbers
   -> data/processed/superstore_clean.csv
   -> scripts/eda.py              KPIs, monthly trend, category / region / top-product summaries, charts
   -> reports/*.csv, reports/charts/*.png
   -> scripts/import_to_mysql.py  validate the CSV and load it into MySQL
   -> sql/business_questions.sql  17 business questions
   -> powerbi/Superstore_Sales_Dashboard.pbix
```

## Key findings

All figures come from `data/processed/superstore_clean.csv` and can be reproduced with the queries in `sql/business_questions.sql`.

1. **Overall:** sales of 2,297,201 and profit of 286,397, a 12.47% margin, across 5,009 orders (average order value about 459). Sales grew from 484K in 2014 to 733K in 2017, with the strongest growth in 2016 (+29.5%) and 2017 (+20.4%).
2. **Furniture sells a lot but earns very little.** It has 741,999 in sales (second highest) but only 18,451 profit, a 2.5% margin. Technology (17.4%) and Office Supplies (17.0%) are far healthier.
3. **Tables and Bookcases lose money.** Tables lose 17,725 on 206,966 in sales (-8.6% margin) and Bookcases lose 3,473. Their average discounts are 26% and 21%, higher than the 16% overall average.
4. **Discounts above 20% are where profit disappears.** Rows with no discount have a 29.5% margin. Rows with a 21-30% discount lose 10,369, 31-50% lose 48,448 and 50%+ lose 76,559, about 135K in total. 72% of all loss-making rows (1,348 of 1,871) had a discount above 20%.
5. **Central region underperforms.** It has the lowest margin (7.9% against 14.9% for West) and the highest average discount (24% against 11-15% elsewhere), which fits the discount finding above.
6. **Sales are seasonal.** September, November and December run at about 1.6x to 1.8x the monthly average, while January and February are the weakest months (about 0.3x to 0.5x).
7. **Product-level risk.** 301 of 1,850 products lose money overall. The largest losses are the Cubify CubeX 3D Printer (double head, -8,880), the Lexmark MX611dhe laser printer (-4,590) and the Cubify CubeX 3D Printer (triple head, -3,840). The best earner is the Canon imageCLASS 2200 copier (25,200 profit on 61,600 sales).

**Suggested actions** (these follow from the data, but the data alone doesn't prove cause): cap discounts at around 20% and review the Tables and Bookcases pricing; check why Central discounts so heavily; review pricing or sourcing for the loss-making printers; plan stock and staffing for September to December.

## Dashboard

The Power BI dashboard (`powerbi/Superstore_Sales_Dashboard.pbix`) shows total sales, total profit, total orders and profit margin, a monthly sales trend, and sales by region, category and sub-category, with category and region slicers.

## SQL highlights

`sql/business_questions.sql` covers KPIs, category / region / segment performance, loss-making products and sub-categories, discount bands, and window-function queries: month-over-month and year-over-year growth with `LAG()`, and top 3 products per category with `ROW_NUMBER()`. Window functions need MySQL 8 or later.

## Repository structure

```
data/raw/            original Excel file
data/processed/      cleaned CSV
scripts/             clean_data.py, eda.py, import_to_mysql.py
sql/                 schema.sql, business_questions.sql
reports/             summary CSVs and charts from eda.py
powerbi/             .pbix dashboard and DAX reference
images/              dashboard screenshot
```

## How to run

1. Install the dependencies: `pip install -r requirements.txt`
2. Clean the data: `python scripts/clean_data.py`
3. Run the EDA: `python scripts/eda.py`
4. Create the database and table in MySQL: run `sql/schema.sql`
5. Load the data: `python scripts/import_to_mysql.py` (asks for your MySQL root password)
6. Run the queries in `sql/business_questions.sql`
7. Open `powerbi/Superstore_Sales_Dashboard.pbix` in Power BI Desktop

## Author

Eithem Shashank, B.Tech Computer Science (AI & ML), aspiring Data Analyst. [GitHub](https://github.com/eithemshashank)
