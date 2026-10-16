WITH ordered_sales AS (
    SELECT 
        f.order_id,
        f.customer_id,
        c.company_name,
        f.date_key,
        f.line_total,
        -- Assigns 1 to the customers earliest order, 2 to their second, etc.
        ROW_NUMBER() OVER (
            PARTITION BY f.customer_id 
            ORDER BY f.date_key, f.order_id
        ) AS purchase_sequence
    FROM fact_sales f
    JOIN dim_customers c ON f.customer_id = c.customer_id
)
SELECT 
    order_id,
    company_name,
    date_key,
    line_total,
    purchase_sequence,
    -- Conditional classification tag
    CASE 
        WHEN purchase_sequence = 1 THEN 'First Purchase'
        ELSE 'Repeat Purchase'
    END AS purchase_type
FROM ordered_sales
ORDER BY customer_id, purchase_sequence;