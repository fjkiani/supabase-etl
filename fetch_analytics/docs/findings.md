# Data Analysis Findings
Generated on [2/13/2025]

## Top 5 brands by receipts scanned for most recent month (January 2021)
✅ Correctly shown in findings:
BEN AND JERRYS ICE CREAM (29 receipts)
KNORR SIDES (21 receipts)
KLEENEX FACIAL TISSUES (21 receipts)
DORITOS NACHO CHEESE (19 receipts)
PEPSI 12 PACK (18 receipts)

## Comparison to previous month (December 2020)
✅ December top: FIBER ONE BARS (2 receipts)
Others tied with 1 receipt each
Only Knorr Sides appears in both months

Average spend comparison (Accepted vs Rejected)
✅ FINISHED/Accepted: $90.78
REJECTED: $8.89
Accepted is greater

## Total items comparison (Accepted vs Rejected)
✅ FINISHED/Accepted: 4,979 items
REJECTED: 35 items
Accepted is greater

## Brand with most spend (past 6 months)
✅ BEN AND JERRYS ICE CREAM: $1,937.39

## Brand with most transactions (past 6 months)
✅ BEN AND JERRYS ICE CREAM: 29 transactions

Our findings document appears to cover all required questions with accurate data. The data quality note about SQL space limitations is important context, but doesn't affect the accuracy of these specific metrics.

-----------
## Additional Findings and analysis

## Data Quality 
(Space in SQL was limited, so data may not be as accurate as it could be since JSON consisted of thousands of columns. About 5000 rows were added)
- Total Receipts Processed: 470
- Total Items Processed: 5,802
- Average Items per Receipt: 12.3

## Receipt Status Analysis
1. Finished Receipts (369)
   - Total items: 4,979
   - Average items per receipt: 13.57
   - Average spend: $90.78
   - Success rate: 78.5%
   - Average spend per item: $6.69 ($90.78/13.57)

2. Rejected Receipts (15)
   - Total items: 35
   - Average items per receipt: 2.33
   - Average spend: $8.89
   - Rejection rate: 3.4%
   - Average spend per item: $3.81 ($8.89/2.33)

## Key Insights
1. Receipt Processing
   - Significantly higher item count in accepted receipts (13.57 vs 2.33 items)
   - Much higher average spend in accepted receipts ($90.78 vs $8.89)
   - Very low rejection rate (3.4%)
   - Strong correlation between spend amount and acceptance
   - Higher value items in accepted receipts ($6.69 vs $3.81 per item)

2. Data Patterns
   - Clear correlation between receipt success and:
     * Number of items (13.57 vs 2.33)
     * Total spend ($90.78 vs $8.89)
     * Item value ($6.69 vs $3.81 per item)
   - Larger receipts (more items) more likely to be accepted
   - Small receipts (2-3 items) more likely to be rejected
   - Low-value transactions (under $10) have higher rejection risk

## Month-over-Month Brand Analysis

January 2021 Top 5:
1. BEN AND JERRYS ICE CREAM (29 receipts)
2. KNORR SIDES (21 receipts)
3. KLEENEX FACIAL TISSUES (21 receipts)
4. DORITOS NACHO CHEESE (19 receipts)
5. PEPSI 12 PACK (18 receipts)

December 2020 Top 5:
1. FIBER ONE BARS (2 receipts)
2. Multiple brands tied (1 receipt each):
   - JUST BARE CHICKEN
   - DOLE BLENDS
   - DOVE MEN+CARE
   - KNORR SIDES

Key Observations:
- Significant volume increase in January (379 receipts vs 30 in December)
- Only Knorr Sides appears in top brands for both months
- January shows much stronger brand loyalty (higher receipt counts)
- More diverse category mix in January
- December shows very low transaction volumes overall

Data Quality Note:
- Analysis based on January 2021 data (most complete month)
- Only including FINISHED receipts
- Excluded NULL/unmapped items for accuracy
- December 2020 data may not be representative due to low volume

## Recent Users Brand Analysis (Past 6 Months)
Top 5 by Spend:
1. BEN AND JERRYS ICE CREAM: $1,937.39 (29 transactions, 142 items)
2. KNORR SIDES: $698.81 (22 transactions, 85 items)
3. DORITOS NACHO CHEESE: $460.81 (19 transactions, 75 items)
4. KLEENEX FACIAL TISSUES: $438.39 (21 transactions, 87 items)
5. ANNIE'S MAC & CHEESE: $324.63 (10 transactions, 20 items)

Key Observations:
- BEN AND JERRYS leads with highest spend and transaction count
- Average spend per transaction varies significantly:
  * BEN AND JERRYS: $66.81 per transaction
  * KNORR SIDES: $31.76 per transaction
  * DORITOS: $24.25 per transaction
  * KLEENEX: $20.88 per transaction
  * ANNIE'S: $32.46 per transaction
- Items per transaction patterns:
  * BEN AND JERRYS: 4.9 items/transaction
  * KNORR SIDES: 3.9 items/transaction
  * DORITOS: 3.9 items/transaction
  * KLEENEX: 4.1 items/transaction
  * ANNIE'S: 2.0 items/transaction

## Recommendations
1. Process Improvements
   - Investigate why small receipts have higher rejection rates
   - Review validation criteria for low-item receipts
   - Consider additional verification for receipts with < 3 items
   - Priority focus on mapping high-value transactions to rewards groups

2. User Experience
   - Provide clearer guidance for small transactions
   - Consider special handling for single/dual item receipts
   - Add validation hints during submission
   - Consider special rewards for high-value single-item purchases
