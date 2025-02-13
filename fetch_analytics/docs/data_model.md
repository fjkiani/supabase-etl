# Data Model Documentation

## Overview
This document describes the relational data model for the Fetch Rewards receipt data warehouse.

## Tables

### Receipts
Main table storing receipt metadata and transaction information.

**Fields:**
- receipt_id (PK): Unique identifier for each receipt
- user_id: Reference to the user who submitted the receipt
- rewards_receipt_status: Current status of the receipt
- total_spent: Total amount spent on the receipt
- points_earned: Total points earned from the receipt
- bonus_points_earned: Additional bonus points earned
- bonus_points_reason: Reason for bonus points
- purchase_date: Date of purchase
- create_date: Receipt creation date
- date_scanned: When the receipt was scanned
- finished_date: When processing was completed
- modify_date: Last modification date
- points_awarded_date: When points were awarded
- purchased_item_count: Number of items on receipt

### Receipt Items
Detailed information about individual items on receipts.

**Fields:**
- item_id (PK): Unique identifier for each item
- receipt_id (FK): Reference to parent receipt
- barcode: Product barcode
- description: Product description
- final_price: Final price paid
- item_price: Original item price
- needs_fetch_review: Flag for items needing review
- partner_item_id: Partner's item identifier
- prevent_target_gap_points: Points restriction flag
- quantity_purchased: Quantity of item purchased
- rewards_group: Brand/category grouping
- rewards_product_partner_id: Partner's product identifier 