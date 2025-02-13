import json
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def generate_findings():
    # Get data
    receipts = supabase.table('receipts').select('*').execute()
    items = supabase.table('receipt_items').select('*').execute()
    
    # Calculate metrics
    total_receipts = len(receipts.data)
    total_items = len(items.data)
    
    # Generate findings document
    findings = f"""# Data Analysis Findings
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Quality
- Total Receipts Processed: {total_receipts:,}
- Total Items Processed: {total_items:,}
- Average Items per Receipt: {total_items/total_receipts:.1f}

## Key Metrics
1. Receipt Processing
   - Finished: {sum(1 for r in receipts.data if r['rewards_receipt_status'] == 'FINISHED')}
   - Rejected: {sum(1 for r in receipts.data if r['rewards_receipt_status'] == 'REJECTED')}
   - Pending: {sum(1 for r in receipts.data if r['rewards_receipt_status'] == 'PENDING')}

2. Financial Impact
   - Total Spend: ${sum(float(r['total_spent'] or 0) for r in receipts.data):,.2f}
   - Average Spend per Receipt: ${sum(float(r['total_spent'] or 0) for r in receipts.data)/total_receipts:.2f}

## Recommendations
1. Data Collection
   - Implement standardized brand naming
   - Add validation for price fields
   - Enhance date validation

2. Business Operations
   - Focus on top performing brands
   - Optimize receipt processing time
   - Improve user engagement through points system
"""
    
    # Write to file
    with open('../docs/findings.md', 'w') as f:
        f.write(findings)
    
    print("Findings document generated!")

if __name__ == "__main__":
    generate_findings() 