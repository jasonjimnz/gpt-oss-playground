-- Purpose: Calculate the total revenue per customer from both banking deposits and e-commerce purchases.
-- Structure: This query joins the aggregated customer dimension with the banking and order fact tables.
-- It uses COALESCE to handle customers who may only have data in one of the services.
-- It sums the total amounts from both sources to provide a combined total.
SELECT
    ac.customer_key,
    CONCAT(ac.first_name, ' ', ac.last_name) AS name,
    COALESCE(SUM(b.amount), 0) AS bank_deposits,
    COALESCE(SUM(o.total_amount), 0) AS ecommerce_revenue,
    COALESCE(SUM(b.amount), 0) + COALESCE(SUM(o.total_amount), 0) AS total_spend
FROM
    analytics_customer ac
LEFT JOIN
    analytics_fct_banking b ON ac.customer_key = b.customer_key AND b.type = 'DEPOSIT'
LEFT JOIN
    analytics_fct_order o ON ac.customer_key = o.customer_key
GROUP BY
    ac.customer_key, name;