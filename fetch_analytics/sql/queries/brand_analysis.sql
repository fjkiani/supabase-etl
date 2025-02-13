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

WITH months AS (
    SELECT 
        DATE_TRUNC('month', purchase_date) as month
    FROM receipts
    GROUP BY DATE_TRUNC('month', purchase_date)
    ORDER BY month DESC
    LIMIT 2
)
SELECT 
    ri.rewards_group as brand,
    DATE_TRUNC('month', r.purchase_date) as month,
    COUNT(DISTINCT r.receipt_id) as receipt_count,
    RANK() OVER (PARTITION BY DATE_TRUNC('month', r.purchase_date) 
                 ORDER BY COUNT(DISTINCT r.receipt_id) DESC) as rank
FROM receipts r
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
WHERE DATE_TRUNC('month', r.purchase_date) IN (SELECT month FROM months)
GROUP BY ri.rewards_group, DATE_TRUNC('month', r.purchase_date)
HAVING COUNT(DISTINCT r.receipt_id) > 0
ORDER BY month DESC, receipt_count DESC;

SELECT 
    r.rewards_receipt_status,
    COUNT(ri.item_id) as total_items,
    COUNT(DISTINCT r.receipt_id) as receipt_count,
    COUNT(ri.item_id)::float / COUNT(DISTINCT r.receipt_id) as avg_items_per_receipt
FROM receipts r
LEFT JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
WHERE r.rewards_receipt_status IN ('FINISHED', 'REJECTED')
GROUP BY r.rewards_receipt_status;

WITH recent_users AS (
    SELECT DISTINCT user_id
    FROM receipts
    WHERE create_date >= NOW() - INTERVAL '6 months'
)
SELECT 
    ri.rewards_group as brand,
    COUNT(DISTINCT r.receipt_id) as transaction_count,
    SUM(ri.final_price) as total_spend
FROM receipts r
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
WHERE r.user_id IN (SELECT user_id FROM recent_users)
GROUP BY ri.rewards_group
ORDER BY total_spend DESC, transaction_count DESC
LIMIT 5; 