-- Purpose: Calculate the Return on Investment (ROI) for marketing campaigns by channel.
-- Structure: This query assumes a marketing fact table exists. It joins this with the order fact table
-- on the month of the campaign and order. It calculates total spend, total revenue, and ROI per channel.
-- NULLIF is used to prevent division by zero errors.
-- Assumes a marketing_campaign fact table exists.
SELECT
    m.channel,
    SUM(m.spend_amount) AS spend,
    COALESCE(SUM(o.total_amount), 0) AS revenue_from_orders,
    (COALESCE(SUM(o.total_amount), 0) - SUM(m.spend_amount)) / NULLIF(SUM(m.spend_amount), 0) AS roi
FROM
    marketing_campaign m
LEFT JOIN
    analytics_fct_order o ON DATE_TRUNC('month', o.order_date) = DATE_TRUNC('month', m.month)
GROUP BY
    m.channel;