import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

def run_and_save_analysis():
    # Read queries from brand_analysis.sql
    with open('../sql/queries/brand_analysis.sql', 'r') as file:
        queries = file.read().split(';')
    
    results = []
    for query in queries:
        if query.strip():
            # Execute the actual SQL query
            data = supabase.rpc('run_query', {'query': query.strip()}).execute()
            results.append(data)
    
    # Generate markdown with actual results
    with open('../docs/query_results.md', 'w') as f:
        f.write(f"# SQL Analysis Results\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for i, result in enumerate(results):
            f.write(f"## Query {i+1} Results\n")
            f.write("```\n")
            # Format the results in a readable way
            if result.data:
                for row in result.data:
                    f.write(f"{row}\n")
            f.write("\n```\n\n")

if __name__ == "__main__":
    run_and_save_analysis() 