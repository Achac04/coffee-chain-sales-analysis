Q0. Look at the tables

SELECT * FROM sales LIMIT 10;
Q1. Total revenue and orders

SELECT
  COUNT(*) AS orders,
  ROUND(SUM(s.quantity * p.price * (1 - s.discount)), 2) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id;
Q2. Revenue by category and product (JOIN + GROUP BY)

SELECT p.category, p.product_name,
       ROUND(SUM(s.quantity * p.price * (1 - s.discount)), 2) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category, p.product_name
ORDER BY revenue DESC;
Q3. Revenue by city

SELECT st.city,
       COUNT(*) AS orders,
       ROUND(SUM(s.quantity * p.price * (1 - s.discount)), 2) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN stores st ON s.store_id = st.store_id
GROUP BY st.city
ORDER BY revenue DESC;
Q4. Monthly revenue and month-over-month growth (CTE + window function)

WITH monthly AS (
  SELECT strftime('%Y-%m', s.order_date) AS month,
         SUM(s.quantity * p.price * (1 - s.discount)) AS revenue
  FROM sales s
  JOIN products p ON s.product_id = p.product_id
  GROUP BY month
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / LAG(revenue) OVER (ORDER BY month), 1) AS mom_growth_pct
FROM monthly;
Q5. Top 3 stores in each city (RANK)

WITH store_rev AS (
  SELECT st.city, st.store_name,
         SUM(s.quantity * p.price * (1 - s.discount)) AS revenue
  FROM sales s
  JOIN products p ON s.product_id = p.product_id
  JOIN stores st ON s.store_id = st.store_id
  GROUP BY st.city, st.store_name
)
SELECT * FROM (
  SELECT city, store_name, ROUND(revenue, 2) AS revenue,
         RANK() OVER (PARTITION BY city ORDER BY revenue DESC) AS rnk
  FROM store_rev
)
WHERE rnk <= 3;
Q6. Do discounts help? (average units per order by discount level)

SELECT discount, COUNT(*) AS orders, ROUND(AVG(quantity), 2) AS avg_units
FROM sales
GROUP BY discount;
Because the data is random, you will likely see little difference. That is a finding too: "discounts did not increase units per order, so they cost margin." Practice saying it.

Q7. Create a reusable view and export it for Power BI

CREATE VIEW v_sales_enriched AS
SELECT s.order_id, s.order_date, st.city, st.store_name,
       p.product_name, p.category, s.quantity, p.price, s.discount,
       ROUND(s.quantity * p.price * (1 - s.discount), 2) AS revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN stores st ON s.store_id = st.store_id;