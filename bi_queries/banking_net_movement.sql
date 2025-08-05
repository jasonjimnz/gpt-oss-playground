-- Purpose: Calculate the net movement of funds for each bank account.
-- Structure: This query joins the bank_account and bank_transaction tables.
-- It uses a CASE statement to sum deposits as positive amounts and withdrawals
-- as negative amounts to calculate the net change. The result is grouped by account.
SELECT
    a.account_id,
    a.balance,
    SUM(CASE
            WHEN t.type = 'DEPOSIT' THEN t.amount
            WHEN t.type = 'WITHDRAWAL' THEN -t.amount
        END) AS net_change
FROM
    bank_account a
LEFT JOIN
    bank_transaction t ON a.account_id = t.account_id
GROUP BY
    a.account_id, a.balance;