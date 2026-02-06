import yfinance as yf
import json
import pandas as pd
from datetime import datetime, timedelta
import os

# S&P 500 Sectors - Vanguard ETFs
SECTORS = ['VGT', 'VHT', 'VFH', 'VCR', 'VOX', 'VIS', 'VDC', 'VDE', 'VPU', 'VNQ', 'VAW']

print("Fetching S&P 500 sector data...")

# Fetch 5 years of data
end_date = datetime.now()
start_date = end_date - timedelta(days=1825)

data = yf.download(SECTORS, start=start_date, end=end_date)['Close']

# Convert to JSON-friendly format
result = {}
for ticker in SECTORS:
    result[ticker] = [
        {"date": date.strftime("%Y-%m-%d"), "price": round(price, 2)}
        for date, price in zip(data.index, data[ticker])
        if not pd.isna(price)
    ]

# Save to JSON (use relative path for GitHub Actions compatibility)
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'stock_data.json')

with open(output_path, 'w') as f:
    json.dump(result, f)

print(f"Data saved to {output_path}")
print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
