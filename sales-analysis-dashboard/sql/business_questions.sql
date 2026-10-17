
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
