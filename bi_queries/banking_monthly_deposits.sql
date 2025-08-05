-- Purpose: Calculate the total deposits per month for the last 12 months.
-- Structure: This query truncates the transaction date to the beginning of the month.
-- It then sums the transaction amounts, filtering only for 'DEPOSIT' types.
-- The query groups the results by month and orders them chronologically.
SELECT
    date_trunc('month', transaction_date) AS month,
    SUM(amount) FILTER (WHERE type = 'DEPOSIT') AS total_deposits
FROM
    bank_transaction
WHERE
    transaction_date >= now() - interval '12 months'
GROUP BY
    month
ORDER BY
    month;