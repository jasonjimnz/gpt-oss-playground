-- Purpose: Estimate the Customer Lifetime Value (LTV) based on purchase history.
-- Structure: This query uses a Common Table Expression (CTE) to calculate total spend,
-- order count, and average days between orders for each customer. The main query then
-- uses these metrics to provide a simple one-year LTV projection.
WITH purchase_history AS (
    SELECT
        ac.customer_key,
        SUM(o.total_amount) AS total_spent,
        COUNT(DISTINCT o.order_id) AS orders_cnt,
        AVG(EXTRACT(EPOCH FROM (o.order_date - MIN(o.order_date) OVER (PARTITION BY ac.customer_key ORDER BY o.order_date))) / 86400.0) AS avg_days_between_orders
    FROM
        analytics_customer ac
    JOIN
        analytics_fct_order o ON ac.customer_key = o.customer_key
    GROUP BY
        ac.customer_key
)
SELECT
    customer_key,
    total_spent,
    orders_cnt,
    (total_spent / NULLIF(orders_cnt, 0)) * 12 AS ltv_estimate_simple_1_year_projection
FROM
    purchase_history;