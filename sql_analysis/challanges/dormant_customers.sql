/*
 Find any customers who have never placed a single order.
 */

SELECT
    c.customer_id,
    c.company_name,
    c.country
FROM dim_customers c
LEFT JOIN fact_sales f ON c.customer_id = f.customer_id
-- The anti join condition:keep only rows where the match in fact_sales resulted in null
WHERE f.order_id IS NULL;