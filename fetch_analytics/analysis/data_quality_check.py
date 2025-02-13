import pandas as pd
import json
from datetime import datetime

def check_data_quality():
    issues = []
    
    # Load data
    with open('../data/raw/receipts.json', 'r') as file:
        receipts = [json.loads(line) for line in file]
    
    for receipt in receipts:
        # Check required fields
        if not receipt.get('_id'):
            issues.append(f"Missing _id in receipt")
        
        if not receipt.get('userId'):
            issues.append(f"Missing userId in receipt {receipt['_id']}")
        
        # Check date consistency
        dates = {
            'createDate': receipt.get('createDate'),
            'dateScanned': receipt.get('dateScanned'),
            'purchaseDate': receipt.get('purchaseDate'),
            'finishedDate': receipt.get('finishedDate'),
            'modifyDate': receipt.get('modifyDate')
        }
        
        # Convert dates for comparison
        parsed_dates = {}
        for key, value in dates.items():
            if value and isinstance(value, dict) and '$date' in value:
                parsed_dates[key] = datetime.fromtimestamp(value['$date']/1000)
        
        if parsed_dates.get('finishedDate') and parsed_dates.get('createDate'):
            if parsed_dates['finishedDate'] < parsed_dates['createDate']:
                issues.append(f"Invalid date sequence in receipt {receipt['_id']}")
        
        # Check items
        if 'rewardsReceiptItemList' in receipt:
            items = receipt['rewardsReceiptItemList']
            for item in items:
                # Price validation
                try:
                    if float(item.get('finalPrice', 0)) > float(item.get('itemPrice', 0)):
                        issues.append(f"Final price greater than item price in receipt {receipt['_id']}")
                except (ValueError, TypeError):
                    issues.append(f"Invalid price format in receipt {receipt['_id']}")
                
                # Quantity validation
                if item.get('quantityPurchased', 0) <= 0:
                    issues.append(f"Invalid quantity in receipt {receipt['_id']}")
    
    return issues

if __name__ == "__main__":
    issues = check_data_quality()
    print("\nData Quality Issues Found:")
    for issue in issues:
        print(f"- {issue}") 