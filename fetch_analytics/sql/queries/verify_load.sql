-- Check receipt counts
SELECT rewards_receipt_status, COUNT(*) 
FROM receipts 
GROUP BY rewards_receipt_status;

-- Check item counts and averages
SELECT 
    COUNT(*) as total_items,
    COUNT(DISTINCT receipt_id) as unique_receipts,
    AVG(quantity_purchased) as avg_quantity,
    COUNT(DISTINCT rewards_group) as unique_brands
FROM receipt_items; 