import json
import pandas as pd
from collections import defaultdict
import datetime
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def analyze_loaded_data():
    """Analyze the data in Supabase"""
    print("\n=== Analyzing Loaded Data ===")
    
    # Get receipt statistics
    receipts = supabase.table('receipts').select('*').execute()
    items = supabase.table('receipt_items').select('*').execute()
    
    print("\nData Quality Summary:")
    print(f"Total Receipts: {len(receipts.data)}")
    print(f"Total Items: {len(items.data)}")
    
    # Status distribution
    status_counts = {}
    for receipt in receipts.data:
        status = receipt['rewards_receipt_status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nReceipt Status Distribution:")
    for status, count in status_counts.items():
        print(f"{status}: {count}")
    
    # Analyze spend patterns
    print("\nSpend Analysis:")
    total_spent = sum(float(r['total_spent'] or 0) for r in receipts.data)
    avg_spent = total_spent / len(receipts.data)
    print(f"Total Spend: ${total_spent:,.2f}")
    print(f"Average Spend per Receipt: ${avg_spent:.2f}")
    
    # Brand analysis
    brand_counts = {}
    for item in items.data:
        brand = item['rewards_group']
        if brand:
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    print("\nTop 5 Brands by Item Count:")
    top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for brand, count in top_brands:
        print(f"{brand}: {count} items")

def analyze_json_structure():
    # Load JSON data
    with open('../data/raw/receipts.json', 'r') as file:
        # Read line by line since each line is a separate JSON object
        receipts = [json.loads(line) for line in file]
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(receipts)
    
    # Analyze basic structure
    print("\n=== Basic Statistics ===")
    print(f"Total number of receipts: {len(df)}")
    print("\n=== Column Names and Data Types ===")
    print(df.dtypes)
    
    # Analyze receipt status values
    print("\n=== Receipt Status Values ===")
    print(df['rewardsReceiptStatus'].value_counts())
    
    # Analyze date ranges
    print("\n=== Date Ranges ===")
    for col in df.columns:
        if 'date' in col.lower():
            print(f"\n{col}:")
            try:
                dates = pd.to_datetime(df[col].apply(lambda x: x.get('$date') if isinstance(x, dict) else x))
                print(f"Min date: {dates.min()}")
                print(f"Max date: {dates.max()}")
            except:
                print("Could not parse dates")
    
    # Analyze receipt items
    print("\n=== Receipt Items Analysis ===")
    item_fields = defaultdict(set)
    total_items = 0
    
    for receipt in receipts:
        if 'rewardsReceiptItemList' in receipt:
            items = receipt['rewardsReceiptItemList']
            total_items += len(items)
            for item in items:
                for key in item.keys():
                    item_fields[key].add(type(item[key]).__name__)
    
    print(f"Total number of items: {total_items}")
    print("\nItem fields and their data types:")
    for field, types in item_fields.items():
        print(f"{field}: {types}")

if __name__ == "__main__":
    print("Running both analyses...")
    analyze_json_structure()
    analyze_loaded_data() 