import requests
from bs4 import BeautifulSoup
import json

urls = [
     "" # add url to check json
]

with open("housing_scraper_output_519_12.json", "w") as outfile:
    for url in urls:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            json_ld_scripts = soup.find_all('script', type='application/ld+json')

            for script in json_ld_scripts:
                try:
                    json_data = json.loads(script.string)
                    
                    json.dump(json_data, outfile, indent=4)
                    outfile.write("\n")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for {url}: {e}")
        else:
            print(f"Failed to retrieve {url}")
