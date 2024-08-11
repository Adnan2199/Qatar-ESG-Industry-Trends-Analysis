import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd

def scrape_and_save(urls, folder):
    for url in urls:
        company_name = url.split('/')[-1]  # Extract the company name from the URL
        page = requests.get(url)
        soup = BeautifulSoup(page.content , 'html.parser')
        table = soup.find('table', class_='data_table')
        rows = table.find_all('tr')
        header_row = next((row for row in rows if "2022" in row.get_text(strip=True)), None)
        table_data = []
        if header_row:
            for row in rows[rows.index(header_row):]:
                row_data = [cell.text.strip() for cell in row.find_all('td')]
                if row_data and row_data[0] not in ['Environment', 'Social', 'Corporate Governance']:
                    # Remove commas from all numeric values
                    row_data = [value.replace(',', '') if value.replace(',', '').replace('.', '').isdigit() else value for value in row_data]
                    table_data.append(row_data)
        csv_file = os.path.join(folder, f'{company_name}.csv')
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(table_data)
        print(f"Data has been saved to {csv_file}.")

def restructure_csv(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder, filename)
            
            # Read CSV file
            df = pd.read_csv(filepath, index_col=0)
            
            # Replace "N / A" values with empty strings
            df.replace("N / A", "", inplace=True)
            
            # Transpose DataFrame
            df_transposed = df.T.reset_index()
            
            # Rename columns
            df_transposed.rename(columns={'index': 'Year'}, inplace=True)
            
            # Add Company column
            company_name = os.path.splitext(filename)[0]
            df_transposed['Company'] = company_name
            
            # Reorder columns
            columns = ['Company'] + list(df_transposed.columns[:-1])
            df_transposed = df_transposed[columns]
            
            # Save to the existing CSV file
            df_transposed.to_csv(filepath, index=False)
            print(f"Data has been saved to {filepath}.")

# Usage
urls = ['https://qse.arabsustainability.com/cbq','https://qse.arabsustainability.com/doha_bank','https://qse.arabsustainability.com/inma','https://qse.arabsustainability.com/nlh','https://qse.arabsustainability.com/qiib','https://qse.arabsustainability.com/qnb','https://qse.arabsustainability.com/ahlibank','https://qse.arabsustainability.com/qib','https://qse.arabsustainability.com/dlala','https://qse.arabsustainability.com/qfirst_bank','https://qse.arabsustainability.com/alrayan','https://qse.arabsustainability.com/alkhalij_bank']
folder = r'C:\Adnan BMS\College\Code\Intern S2\Banking and Financial Services'

# Scrape and save data
scrape_and_save(urls, folder)

# Restructure CSV files
restructure_csv(folder)
