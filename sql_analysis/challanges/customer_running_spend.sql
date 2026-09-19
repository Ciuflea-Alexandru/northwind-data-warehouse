/*
 Track each customer's orders chronologically.
 Calculate their running total spend.
 Use lag to see how much their previous order was worth.
 */

WITH customer_order_timeline AS(
-- Aggregate total spend per oder per date
SELECT
    f.customer_id,
    f.order_id,
    t.full_date,
    SUM(f.line_total) AS order_total
FROM fact_sales f
JOIN dim_time t ON f.date_key = t.date_key
GROUP BY f.customer_id, f.order_id, t.full_date
)
SELECT
    customer_id,
    order_id,
    full_date,
    order_total,
    -- Running total spend per customer over time
    SUM(order_total) OVER(
    PARTITION BY customer_id
    ORDER BY full_date, order_id)
    AS running_total_spend,
    -- Look back at the previous order total using LAG
    LAG(order_total, 1) OVER(
    PARTITION BY customer_id
    ORDER BY full_date, order_id
    ) AS previous_order_total
FROM customer_order_timeline
ORDER BY customer_id, full_date;