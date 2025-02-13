Fetch Analytics Project
Overview
Analysis of receipt processing data for Fetch Rewards, focusing on user shopping patterns, brand performance, and data quality assessment.

Data Sample
Raw Data: 1,119 receipts with approximately 2,500 items
Loaded Data (due to space constraints):
470 receipts (42% of total)
5,802 receipt items
Statistically significant sample for analysis
Project Structure
data/: Raw data files
sql/: SQL schemas and queries
analysis/: Data quality and business analysis
docs/: Documentation and communication
Setup Instructions
Create database schema using sql/schema/create_tables.sql
Create indexes using sql/schema/indexes.sql
Load data from JSON files
Run analysis queries from sql/queries/
Analysis Components
Data model documentation
Data quality assessment
Business metrics queries
Stakeholder communications
Key Findings
Found in docs under technical_analysis.md, stakeholder_communication_md and more
