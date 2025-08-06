SELECT
    m.channel,
    SUM(m.spend_amount) AS spend,
    COALESCE(SUM(o.total_amount), 0) AS revenue_from_orders,
    (COALESCE(SUM(o.total_amount), 0) - SUM(m.spend_amount)) / NULLIF(SUM(m.spend_amount), 0) AS roi
FROM
    Postgres.public."marketing_campaign" m
LEFT JOIN
    Postgres.public."analytics_fct_order" o ON DATE_TRUNC('MONTH', o.order_date) = DATE_TRUNC('MONTH', m."month")
GROUP BY
    m.channel