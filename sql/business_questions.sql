
USE sales_analysis;

-- 1. Overall business KPIs
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(100 * SUM(profit) / SUM(sales), 2) AS profit_margin_pct
FROM superstore;

-- 2. Sales and profit by category
SELECT category,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY category
ORDER BY sales DESC;

-- 3. Monthly sales and profit
SELECT DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY sales_month
ORDER BY sales_month;

-- 4. Regional performance
SELECT region,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY region
ORDER BY sales DESC;

-- 5. Top 10 products by sales
SELECT product_name,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY product_name
ORDER BY sales DESC
LIMIT 10;

-- 6. Top 10 customers by sales
SELECT customer_id, customer_name,
       ROUND(SUM(sales), 2) AS sales
FROM superstore
GROUP BY customer_id, customer_name
ORDER BY sales DESC
LIMIT 10;

-- 7. Profitability by sub-category
SELECT category, sub_category,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit,
       ROUND(100 * SUM(profit) / NULLIF(SUM(sales), 0), 2)
           AS profit_margin_pct
FROM superstore
GROUP BY category, sub_category
ORDER BY profit ASC;

-- 8. Performance by discount band
SELECT
    CASE
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.20 THEN 'Low Discount'
        WHEN discount <= 0.50 THEN 'Medium Discount'
        ELSE 'High Discount'
    END AS discount_band,
    COUNT(*) AS transaction_rows,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY discount_band
ORDER BY profit DESC;

-- 9. Customer segment performance
SELECT segment,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM superstore
GROUP BY segment
ORDER BY sales DESC;

-- 10. Loss-making products
SELECT product_name,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM superstore
GROUP BY product_name
HAVING SUM(profit) < 0
ORDER BY profit ASC
LIMIT 20;

-- 11. Discount impact: finer discount bands (shows where losses begin)
SELECT
    CASE
        WHEN discount = 0 THEN '0%'
        WHEN discount <= 0.10 THEN '1-10%'
        WHEN discount <= 0.20 THEN '11-20%'
        WHEN discount <= 0.30 THEN '21-30%'
        WHEN discount <= 0.50 THEN '31-50%'
        ELSE '50%+'
    END AS discount_band,
    COUNT(*) AS transaction_rows,
    ROUND(SUM(sales), 2) AS sales,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100 * SUM(profit) / SUM(sales), 2) AS profit_margin_pct,
    ROUND(AVG(profit), 2) AS avg_profit_per_row
FROM superstore
GROUP BY discount_band
ORDER BY MIN(discount);

-- 12. Month-over-month sales growth (window function: LAG)
WITH monthly AS (
    SELECT DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
           SUM(sales) AS sales
    FROM superstore
    GROUP BY sales_month
)
SELECT sales_month,
       ROUND(sales, 2) AS sales,
       ROUND(100 * (sales - LAG(sales) OVER (ORDER BY sales_month))
             / LAG(sales) OVER (ORDER BY sales_month), 1) AS mom_growth_pct
FROM monthly
ORDER BY sales_month;

-- 13. Yearly sales, profit and year-over-year growth
WITH yearly AS (
    SELECT YEAR(order_date) AS order_year,
           SUM(sales) AS sales,
           SUM(profit) AS profit
    FROM superstore
    GROUP BY order_year
)
SELECT order_year,
       ROUND(sales, 2) AS sales,
       ROUND(profit, 2) AS profit,
       ROUND(100 * (sales - LAG(sales) OVER (ORDER BY order_year))
             / LAG(sales) OVER (ORDER BY order_year), 1) AS sales_yoy_pct
FROM yearly
ORDER BY order_year;

-- 14. Top 3 products by profit within each category (window function: ROW_NUMBER)
SELECT category, product_name, profit, rank_in_category
FROM (
    SELECT category,
           product_name,
           ROUND(SUM(profit), 2) AS profit,
           ROW_NUMBER() OVER (
               PARTITION BY category ORDER BY SUM(profit) DESC
           ) AS rank_in_category
    FROM superstore
    GROUP BY category, product_name
) ranked
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;

-- 15. Sub-categories that lose money overall
SELECT category, sub_category,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit,
       ROUND(AVG(discount) * 100, 1) AS avg_discount_pct
FROM superstore
GROUP BY category, sub_category
HAVING SUM(profit) < 0
ORDER BY profit ASC;

-- 16. Share of loss-making rows that had a discount above 20%
SELECT COUNT(*) AS loss_making_rows,
       SUM(discount > 0.20) AS rows_with_discount_over_20,
       ROUND(100 * SUM(discount > 0.20) / COUNT(*), 1) AS pct_over_20
FROM superstore
WHERE profit < 0;

-- 17. Average order value (distinct orders, not rows)
SELECT ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM superstore;
