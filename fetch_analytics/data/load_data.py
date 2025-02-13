import json
from supabase import create_client
from datetime import datetime
from decimal import Decimal
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize Supabase client with service role key
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(supabase_url, supabase_key)

def parse_date(date_dict):
    if not date_dict or not isinstance(date_dict, dict):
        return None
    timestamp = date_dict.get('$date')
    if timestamp:
        return datetime.fromtimestamp(timestamp/1000).isoformat()
    return None

def parse_decimal(value):
    if not value:
        return None
    try:
        return float(str(value))
    except:
        return None

def camel_to_snake(name):
    """Convert camelCase to snake_case"""
    import re
    name = re.sub('([A-Z]+)', r'_\1', name).lower()
    return name.strip('_')

def transform_receipt(receipt):
    """Transform receipt data dynamically"""
    # Handle _id specially
    transformed = {
        "receipt_id": receipt['_id']['$oid'],
        "user_id": receipt['userId']
    }
    
    # Map all other fields
    for key, value in receipt.items():
        if key not in ['_id', 'userId', 'rewardsReceiptItemList']:
            db_key = camel_to_snake(key)
            if 'date' in key.lower():
                transformed[db_key] = parse_date(value)
            elif any(x in key.lower() for x in ['price', 'spent', 'earned']):
                transformed[db_key] = parse_decimal(value)
            else:
                transformed[db_key] = value
                
    return transformed

def transform_item(item, receipt_id):
    """Transform item data dynamically"""
    transformed = {"receipt_id": receipt_id}
    
    for key, value in item.items():
        db_key = camel_to_snake(key)
        if any(x in key.lower() for x in ['price', 'earned']):
            transformed[db_key] = parse_decimal(value)
        elif isinstance(value, (bool, int, str)):
            transformed[db_key] = value
            
    return transformed

def load_data():
    receipt_count = 0
    item_count = 0
    error_count = 0
    
    print("Starting data load...")
    
    with open('raw/receipts.json', 'r') as file:
        for line_number, line in enumerate(file, 1):
            try:
                receipt = json.loads(line)
                
                # Transform receipt data dynamically
                receipt_data = transform_receipt(receipt)
                
                # Use upsert instead of insert
                data = supabase.table('receipts').upsert(receipt_data).execute()
                receipt_count += 1
                
                # Handle items
                supabase.table('receipt_items').delete().eq('receipt_id', receipt_data['receipt_id']).execute()
                
                for item in receipt.get('rewardsReceiptItemList', []):
                    try:
                        # Transform item data dynamically
                        item_data = transform_item(item, receipt_data['receipt_id'])
                        
                        supabase.table('receipt_items').insert(item_data).execute()
                        item_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        print(f"Error inserting item for receipt {receipt_data['receipt_id']}: {str(e)}")
                
            except Exception as e:
                error_count += 1
                print(f"Error processing receipt at line {line_number}: {str(e)}")
            
            if line_number % 10 == 0:
                print(f"Processed {line_number} records. Success: {receipt_count}, Errors: {error_count}")
    
    print(f"\nLoad Summary:")
    print(f"Receipts loaded: {receipt_count}")
    print(f"Items loaded: {item_count}")
    print(f"Errors encountered: {error_count}")

if __name__ == "__main__":
    load_data() 