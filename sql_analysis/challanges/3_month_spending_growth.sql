WITH monthly_agg AS(
SELECT
    c.customer_id,
    c.company_name,
    t,year,
    t.month,
    SUM(f.line_total) AS customer_spending
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_time t ON f.date_key = t.date_key
GROUP BY c.customer_id, c.company_name, t, year, t.month
)
SELECT
    customer_id,
    company_name,
    year,
    month,
    customer_spending,
    -- Rolling 3 month spending(current month + preceding 2 months)
    SUM(customer_spending) OVER(
        PARTITION BY customer_id
        ORDER BY year, month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS three_month_spend,
    LAG(customer_spending, 1) OVER(
        PARTITION BY customer_id
        ORDER BY year, month
        ) AS prev_month_spend
FROM monthly_agg
ORDER BY customer_id, year, month;
