# Cleaning and combining FY24 and FY25 budget datasets for Google Sheets
import pandas as pd
from datetime import datetime

# Sample data (replace with actual file loading in production)
fy24_data = pd.read_csv("FY24_Cleaned_CSV - FY24 Amended Budget Ordinance.csv")
fy25_data = pd.read_csv("FY25_Cleaned_CSV - Sheet1.csv")

# Standardizing column names
fy24_data.columns = fy24_data.columns.str.strip().str.replace('_', ' ').str.title()
fy25_data.columns = fy25_data.columns.str.strip().str.replace('_', ' ').str.title()

# Correcting typos in Category (e.g., 'LICESNE FEES' to 'LICENSE FEES')
fy25_data['Category'] = fy25_data['Category'].replace('LICESNE FEES', 'LICENSE FEES')

# Adding Fiscal Year column
fy24_data['Fiscal Year'] = 'FY24'
fy25_data['Fiscal Year'] = 'FY25'

# Combining datasets
combined_data = pd.concat([fy24_data, fy25_data], ignore_index=True)

# Cleaning data: removing any rows with missing critical fields
combined_data = combined_data.dropna(subset=['Category', 'Line Item', 'Amount'])

# Converting Amount to numeric, handling non-numeric values
combined_data['Amount'] = pd.to_numeric(combined_data['Amount'], errors='coerce').fillna(0)

# Saving to CSV for Google Sheets
output_file = f"combined_budget_data_{datetime.now().strftime('%Y%m%d')}.csv"
combined_data.to_csv(output_file, index=False)

print(f"Combined data saved to {output_file}")