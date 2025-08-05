-- Purpose: Identify products where the stock quantity is at or below the reorder point.
-- Structure: This query selects products and uses a CASE statement to flag them
-- with a 'REORDER' status if their stock is low, based on the defined reorder point.
SELECT
    product_id,
    name,
    stock_quantity,
    reorder_point,
    CASE
        WHEN stock_quantity <= reorder_point THEN 'REORDER'
    END AS status
FROM
    ecommerce_product
WHERE
    stock_quantity <= reorder_point;