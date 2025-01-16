import requests
import pandas as pd

# URL to fetch data from
url = "https://webapi.niftytrader.in/webapi/Resource/ban-list"

# Fetch data
response = requests.get(url)

# Check if the response is successful
if response.status_code == 200:
    data = response.json()  # assuming JSON response
    
    # Extract the necessary parts from the resultData
    result_data = data.get('resultData', {})
    securities_ban_list = result_data.get('securities_ban_result', [])
    possible_entrants_list = result_data.get('possible_entrants_result', [])
    possible_exits_list = result_data.get('possible_exits_result', [])
    
    # Add a column to identify the type of list
    for item in securities_ban_list:
        item['list_type'] = 'securities_ban_result'
    
    for item in possible_entrants_list:
        item['list_type'] = 'possible_entrants_result'
    
    for item in possible_exits_list:
        item['list_type'] = 'possible_exits_result'
    
    # Combine all lists into one
    combined_data = securities_ban_list + possible_entrants_list + possible_exits_list
    
    # Convert to a single DataFrame
    df_combined = pd.DataFrame(combined_data)
    
    # Save the combined DataFrame to a single CSV file
    df_combined.to_csv("combined_ban_list.csv", index=False)
    print("Combined data saved to 'combined_ban_list.csv'.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)
