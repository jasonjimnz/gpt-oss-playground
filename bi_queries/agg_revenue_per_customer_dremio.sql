WITH CustomerOrderCalculations AS (
    SELECT
        ac.customer_key,
        o.order_key,
        o.total_amount,
        MIN(o.order_date) OVER (PARTITION BY ac.customer_key) AS first_order_date,
        o.order_date
    FROM
        Postgres.public."analytics_customer" ac
    JOIN
        Postgres.public."analytics_fct_order" o ON ac.customer_key = o.customer_key
) SELECT
    customer_key,
    SUM(total_amount) AS total_spent,
    COUNT(DISTINCT order_key) AS orders_cnt,
    AVG(EXTRACT(EPOCH FROM (order_date - first_order_date)) / 86400.0) AS avg_days_between_orders,
    (SUM(total_amount) / NULLIF(COUNT(DISTINCT order_key), 0)) * 12 AS ltv_estimate_simple_1_year_projection
FROM CustomerOrderCalculations GROUP BY customer_key;