-- Create indexes for performance optimization

-- Receipts table indexes
CREATE INDEX idx_receipts_user_id ON receipts(user_id);
CREATE INDEX idx_receipts_status ON receipts(rewards_receipt_status);
CREATE INDEX idx_receipts_purchase_date ON receipts(purchase_date);

-- Receipt Items table indexes
CREATE INDEX idx_receipt_items_receipt_id ON receipt_items(receipt_id);
CREATE INDEX idx_receipt_items_barcode ON receipt_items(barcode);
CREATE INDEX idx_receipt_items_rewards_group ON receipt_items(rewards_group); 