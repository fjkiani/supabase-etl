import json
from collections import defaultdict

def validate_schema():
    # Load JSON data
    with open('../data/raw/receipts.json', 'r') as file:
        receipts = [json.loads(line) for line in file]
    
    # Analyze schema requirements
    receipt_fields = defaultdict(set)
    item_fields = defaultdict(set)
    
    # Collect all fields and their value types
    for receipt in receipts:
        for key, value in receipt.items():
            receipt_fields[key].add(type(value).__name__)
            
        if 'rewardsReceiptItemList' in receipt:
            for item in receipt['rewardsReceiptItemList']:
                for key, value in item.items():
                    item_fields[key].add(type(value).__name__)
    
    print("=== Receipt Fields Analysis ===")
    for field, types in receipt_fields.items():
        print(f"{field}: {types}")
    
    print("\n=== Receipt Items Fields Analysis ===")
    for field, types in item_fields.items():
        print(f"{field}: {types}")
    
    # Validate specific requirements
    print("\n=== Data Validation Issues ===")
    
    for receipt in receipts:
        # Check for required fields
        if '_id' not in receipt:
            print(f"Missing _id in receipt")
        
        if 'rewardsReceiptItemList' in receipt:
            for item in receipt['rewardsReceiptItemList']:
                # Check for price consistency
                if 'finalPrice' in item and 'itemPrice' in item:
                    try:
                        if float(item['finalPrice']) > float(item['itemPrice']):
                            print(f"Final price greater than item price in receipt {receipt['_id']}")
                    except ValueError:
                        print(f"Invalid price format in receipt {receipt['_id']}")

if __name__ == "__main__":
    validate_schema() 