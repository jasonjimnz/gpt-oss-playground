-- Purpose: List the top 10 best-selling products by units sold.
-- Structure: This query joins the product and order_item tables.
-- It calculates the total units sold and the total revenue for each product.
-- The results are ordered by the number of units sold in descending order to find the top 10.
SELECT
    p.product_id,
    p.name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.line_total) AS revenue
FROM
    ecommerce_product p
JOIN
    ecommerce_order_item oi ON p.product_id = oi.product_id
GROUP BY
    p.product_id, p.name
ORDER BY
    units_sold DESC
LIMIT 10;