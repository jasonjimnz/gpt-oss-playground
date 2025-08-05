-- Purpose: Calculate the monthly sales revenue from the last year.
-- Structure: This query truncates the order date to the month.
-- It sums the total amount for orders that are 'SHIPPED' or 'DELIVERED'.
-- The results are grouped by month and ordered chronologically.
SELECT
    date_trunc('month', o.order_date) AS month,
    SUM(o.total_amount) AS revenue
FROM
    ecommerce_order o
WHERE
    o.order_date >= now() - interval '12 months'
    AND o.status IN ('SHIPPED', 'DELIVERED')
GROUP BY
    month
ORDER BY
    month;