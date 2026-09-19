/*
 Pull a clean restricted list of each customer's first two largest transactions.
 */

WITH ranked_customer_orders AS (
    SELECT
        f.customer_id,
        f.order_id,
        SUM(f.line_total) AS order_total,
        -- ROW_NUMBER assigns a unique sequential rank per customer, ordered by largest spend
        ROW_NUMBER() OVER(
        PARTITION BY f.customer_id
        ORDER BY SUM(f.line_total) DESC
        ) AS spend_rank
    FROM fact_sales f
    GROUP BY f.customer_id, f.order_id
)
SELECT
    *
FROM ranked_customer_orders
-- Filter to keep only the top 2 largest orders for every single customer
WHERE spend_rank <= 2
ORDER BY customer_id, spend_rank;