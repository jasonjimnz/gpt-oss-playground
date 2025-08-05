-- Purpose: Identify the top 5 customers by their total withdrawal amount.
-- Structure: This query joins the customer, account, and transaction tables.
-- It filters for 'WITHDRAWAL' transactions, sums the amounts for each customer,
-- and then orders the results in descending order to find the top 5.
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS name,
    SUM(t.amount) AS total_withdrawn
FROM
    bank_customer c
JOIN
    bank_account a ON c.customer_id = a.customer_id
JOIN
    bank_transaction t ON a.account_id = t.account_id
WHERE
    t.type = 'WITHDRAWAL'
GROUP BY
    c.customer_id, name
ORDER BY
    total_withdrawn DESC
LIMIT 5;