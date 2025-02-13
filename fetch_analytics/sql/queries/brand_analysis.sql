-- Top 5 brands by receipts scanned for most recent month
WITH recent_month AS (
    SELECT DATE_TRUNC('month', MAX(purchase_date)) as recent_month
    FROM receipts
)
SELECT 
    ri.rewards_group as brand,
    COUNT(DISTINCT r.receipt_id) as receipt_count
FROM receipts r
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
WHERE DATE_TRUNC('month', r.purchase_date) = (SELECT recent_month FROM recent_month)
GROUP BY ri.rewards_group
ORDER BY receipt_count DESC
LIMIT 5;

-- Average spend comparison for Accepted vs Rejected receipts
SELECT 
    rewards_receipt_status,
    AVG(total_spent) as avg_spend,
    COUNT(*) as receipt_count
FROM receipts
WHERE rewards_receipt_status IN ('FINISHED', 'REJECTED')
GROUP BY rewards_receipt_status;

-- Top brands by spend
WITH brand_spend AS (
    SELECT 
        ri.rewards_group,
        COUNT(DISTINCT r.receipt_id) as receipt_count,
        COUNT(*) as item_count,
        SUM(ri.final_price) as total_spend
    FROM receipt_items ri
    JOIN receipts r ON ri.receipt_id = r.receipt_id
    WHERE ri.rewards_group IS NOT NULL
    GROUP BY ri.rewards_group
)
SELECT *
FROM brand_spend
ORDER BY total_spend DESC
LIMIT 10;

-- Brand performance over time
SELECT 
    DATE_TRUNC('month', r.purchase_date) as month,
    ri.rewards_group,
    COUNT(DISTINCT r.receipt_id) as receipt_count,
    SUM(ri.final_price) as total_spend
FROM receipt_items ri
JOIN receipts r ON ri.receipt_id = r.receipt_id
WHERE ri.rewards_group IS NOT NULL
GROUP BY DATE_TRUNC('month', r.purchase_date), ri.rewards_group
ORDER BY month DESC, total_spend DESC; 