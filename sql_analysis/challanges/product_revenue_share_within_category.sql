WITH product_category_aggragation AS (
SELECT
    p.category_name,
    p.product_name,
    SUM(f.line_total) AS product_revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category_name, p.product_name
),
product_total_revenue AS(
SELECT
    category_name,
    product_name,
    product_revenue,
    SUM(product_revenue) OVER(PARTITION BY category_name) AS total_revenue
FROM product_category_aggragation
)
SELECT
    category_name,
    product_name,
    total_revenue,
    product_revenue,
    (product_revenue * 100.0 / total_revenue) AS pct_of_category
FROM product_total_revenue
ORDER BY category_name, product_revenue DESC
