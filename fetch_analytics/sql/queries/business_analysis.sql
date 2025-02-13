-- 1. What are the top 5 brands by receipts scanned for most recent month?
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
    AND ri.rewards_group IS NOT NULL
GROUP BY ri.rewards_group
ORDER BY receipt_count DESC
LIMIT 5;

-- 2. How does the ranking of the top 5 brands by receipts compare to previous month?
WITH months AS (
    SELECT 
        DATE_TRUNC('month', MAX(purchase_date)) as recent_month,
        DATE_TRUNC('month', MAX(purchase_date) - INTERVAL '1 month') as previous_month
    FROM receipts
),
brand_ranks AS (
    SELECT 
        ri.rewards_group as brand,
        COUNT(DISTINCT r.receipt_id) as receipt_count,
        DATE_TRUNC('month', r.purchase_date) as month,
        RANK() OVER (PARTITION BY DATE_TRUNC('month', r.purchase_date) 
                     ORDER BY COUNT(DISTINCT r.receipt_id) DESC) as rank
    FROM receipts r
    JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
    WHERE DATE_TRUNC('month', r.purchase_date) IN (SELECT recent_month FROM months 
                                                  UNION SELECT previous_month FROM months)
        AND ri.rewards_group IS NOT NULL
    GROUP BY ri.rewards_group, DATE_TRUNC('month', r.purchase_date)
)
SELECT 
    brand,
    receipt_count,
    month,
    rank
FROM brand_ranks
WHERE rank <= 5
ORDER BY month DESC, rank;

-- 3. Average spend comparison between Accepted and Rejected receipts
SELECT 
    rewards_receipt_status,
    COUNT(*) as receipt_count,
    AVG(total_spent) as avg_spend,
    SUM(purchased_item_count) as total_items
FROM receipts
WHERE rewards_receipt_status IN ('FINISHED', 'REJECTED')
GROUP BY rewards_receipt_status;

-- 4. Brand spending among recent users
WITH recent_users AS (
    SELECT DISTINCT user_id
    FROM receipts
    WHERE create_date >= NOW() - INTERVAL '6 months'
)
SELECT 
    ri.rewards_group as brand,
    COUNT(DISTINCT r.receipt_id) as transaction_count,
    SUM(ri.final_price * ri.quantity_purchased) as total_spend
FROM receipts r
JOIN receipt_items ri ON r.receipt_id = ri.receipt_id
JOIN recent_users ru ON r.user_id = ru.user_id
WHERE ri.rewards_group IS NOT NULL
GROUP BY ri.rewards_group
ORDER BY total_spend DESC, transaction_count DESC
LIMIT 5; 