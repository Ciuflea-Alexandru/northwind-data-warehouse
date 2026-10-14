WITH customers AS (
    SELECT
    c.customer_id,
    c.company_name,
    SUM(f.line_total) AS total_spend
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY  c.customer_id, c.company_name
    )
SELECT
    customer_id,
    company_name,
    total_spend,
    CASE
        WHEN total_spend > 50000 THEN 'VIP'
        WHEN total_spend BETWEEN 20000 AND 50000 THEN 'MID-TIER'
        ELSE 'STANDARD'
        END AS category
FROM customers
ORDER BY total_spend DESC
