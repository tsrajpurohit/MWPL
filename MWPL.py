import requests
from bs4 import BeautifulSoup
import csv

# URL of the website
url = "https://www.5paisa.com/nse-ban-list"

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com",
}

# Send a GET request with headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Function to extract data from a section
    def extract_data(section_id):
        section = soup.find('div', id=section_id)
        if not section:
            return []
        table = section.find('table')
        rows = table.find_all('tr') if table else []
        return [
            {
                "Stock": row.find_all('td')[0].text.strip(),
                "Value1": row.find_all('td')[1].text.strip(),
                "Value2": row.find_all('td')[2].text.strip(),
            }
            for row in rows
        ]

    # Extract data for each section
    securities_in_ban = extract_data('collapseClose1')
    possible_entrants = extract_data('collapseClose2')
    possible_exits = extract_data('collapseClose3')

    # Combine data with a section label
    data = [
        {"Section": "Securities In Ban", **item} for item in securities_in_ban
    ] + [
        {"Section": "Possible Entrants", **item} for item in possible_entrants
    ] + [
        {"Section": "Possible Exits", **item} for item in possible_exits
    ]

    # Save data to a CSV file
    csv_file = "nse_ban_list.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Section", "Stock", "Value1", "Value2"])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved successfully to {csv_file}")

else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
