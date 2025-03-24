import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
import time
import os

<<<<<<< HEAD
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

=======
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
>>>>>>> dev
BASE_URL = "https://housing.com/in/buy/mumbai/mumbai?page={}"
OUTPUT_EXCEL_FILE = "mumbai_housing_price.xlsx"
MAX_PAGES = 1876
CHECKPOINT_FILE = "last_processed_page.txt"

def get_checkpoint():
<<<<<<< HEAD
=======
    """Reads the last processed page from the checkpoint file."""
>>>>>>> dev
    try:
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, 'r') as f:
                return int(f.read().strip()) + 1
    except Exception as e:
        logging.error(f"Error reading checkpoint: {e}")
    return 1

def save_checkpoint(page_num):
<<<<<<< HEAD
=======
    """Saves the current page number to the checkpoint file."""
>>>>>>> dev
    try:
        with open(CHECKPOINT_FILE, 'w') as f:
            f.write(str(page_num))
    except Exception as e:
        logging.error(f"Error saving checkpoint: {e}")

def get_urls(page_num):
<<<<<<< HEAD
=======
    """Fetches all project URLs from a given page number."""
>>>>>>> dev
    url = BASE_URL.format(page_num)
    logging.info(f"Fetching page {page_num}: {url}")
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve page {page_num}: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        json_ld_scripts = soup.find_all('script', type='application/ld+json')

<<<<<<< HEAD
=======
        # Extract URLs from JSON-LD scripts
>>>>>>> dev
        for script in json_ld_scripts:
            try:
                json_data = json.loads(script.string)
                if isinstance(json_data, list):
                    for item in json_data:
                        if isinstance(item, dict) and item.get("@type") == "ItemList":
                            urls = [
                                (proj.get("position"), proj.get("url"))
                                for proj in item.get("itemListElement", [])
                            ]
                            for pos, url in urls:
                                logging.info(f"Page {page_num} - Position {pos}: {url}")
                            return urls

                elif isinstance(json_data, dict) and json_data.get("@type") == "ItemList":
                    urls = [
                        (proj.get("position"), proj.get("url"))
                        for proj in json_data.get("itemListElement", [])
                    ]
                    for pos, url in urls:
                        logging.info(f"Page {page_num} - Position {pos}: {url}")
                    return urls
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON on page {page_num}: {e}")
    except Exception as e:
        logging.error(f"Failed to parse page {page_num}: {e}")
    
    logging.warning(f"No valid project URLs found on page {page_num}")
    return []

<<<<<<< HEAD
def fetch_json_data(url):
=======
def fetch_json_data(url, position):
    """Fetches JSON data from a given project URL."""
>>>>>>> dev
    logging.info(f"Fetching project data: {url}")
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to retrieve project data from {url}: {e}")
        return None

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
<<<<<<< HEAD
        filtered_script = None

        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if "@type" in item and "ApartmentComplex" in item.get("@type", []) and "Product" in item.get("@type", []):
                            filtered_script = item
                            break
                elif isinstance(data, dict):
                    if "@type" in data and "ApartmentComplex" in data.get("@type", []) and "Product" in data.get("@type", []):
                        filtered_script = data
                        break
            except json.JSONDecodeError:
                continue

        if filtered_script:
            return filtered_script
        else:
            logging.warning(f"No matching script found for {url}")
            return None
=======

        # Extract JSON data
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                logging.info(f"Matching script found for position - {position} {url}")
                return data
            except json.JSONDecodeError:
                continue

        logging.warning(f"No matching script found for position - {position} {url}")
        return None
>>>>>>> dev
    except Exception as e:
        logging.error(f"Failed to parse project data from {url}: {e}")
        return None

<<<<<<< HEAD
def main():
=======
def process_apartment_data(json_data, position, url, all_amenities):
    """Processes JSON data and extracts relevant fields."""
    if not isinstance(json_data, list):
        logging.error(f"Expected list for json_data, got {type(json_data)} at {url}")
        return None

    json_data = next((item for item in json_data if isinstance(item, dict) and '@type' in item and 'Product' in item['@type']), None)

    if not json_data:
        logging.error(f"No valid Product data found at {url}")
        return None

    try:
        name = json_data.get('name', '')
        description = json_data.get('description', '')
        low_price = json_data.get('offers', {}).get('lowPrice', json_data.get('offers', {}).get('price', ''))
        high_price = json_data.get('offers', {}).get('highPrice', '')
        address = json_data.get('geo', {}).get('address', json_data.get('address', ''))
        latitude = json_data.get('geo', {}).get('latitude', '')
        longitude = json_data.get('geo', {}).get('longitude', '')
        brand_founding_date = json_data.get('brand', [{}])[0].get('foundingDate', '') if isinstance(json_data.get('brand'), list) else json_data.get('brand', {}).get('foundingDate', '')
        amenities = json_data.get('amenityFeature', [])

        all_amenities.update(amenities)

        apartment_data = {
            'Position': position,
            'Project URL': url,
            'Name': name,
            'Description': description,
            'Low Price': low_price,
            'High Price': high_price,
            'Address': address,
            'Latitude': latitude,
            'Longitude': longitude,
            'Brand Founding Date': brand_founding_date,
        }
        amenity_data = {f'Amenity_{amenity}': 1 if amenity in amenities else 0 for amenity in all_amenities}
        apartment_data.update(amenity_data)

        return apartment_data

    except Exception as e:
        logging.error(f"Error processing data for {url}: {e}")
        return None

def main():
    """Main function that Run the web scraper and save the data."""
>>>>>>> dev
    all_amenities = set()
    start_page = get_checkpoint()

    try:
        for page_num in range(start_page, MAX_PAGES + 1):
            logging.info(f"Starting page {page_num}")
            urls = get_urls(page_num)
            
            if not urls:
                logging.warning(f"No projects found on page {page_num}")
                continue

            all_data = []  

            for position, url in urls:
                logging.info(f"Page no - {page_num} Processing Position {position} — {url}")
                
<<<<<<< HEAD
                json_data = fetch_json_data(url)

                if json_data:
                    try:
                        name = json_data['name'] if 'name' in json_data else ''
                        description = json_data['description'] if 'description' in json_data else ''
                        low_price = json_data['offers']['lowPrice'] if 'offers' in json_data and 'lowPrice' in json_data['offers'] else ''
                        high_price = json_data['offers']['highPrice'] if 'offers' in json_data and 'highPrice' in json_data['offers'] else ''
                        address = json_data['geo']['address'] if 'geo' in json_data and 'address' in json_data['geo'] else ''
                        latitude = json_data['geo']['latitude'] if 'geo' in json_data and 'latitude' in json_data['geo'] else ''
                        longitude = json_data['geo']['longitude'] if 'geo' in json_data and 'longitude' in json_data['geo'] else ''
                        brand_founding_date = json_data['brand'][0]['foundingDate'] if 'brand' in json_data and json_data['brand'] and 'foundingDate' in json_data['brand'][0] else ''
                        amenities = json_data['amenityFeature'] if 'amenityFeature' in json_data else []

                        all_amenities.update(amenities)

                        apartment_data = {
                            'Position': position,
                            'Project URL': url,
                            'Name': name,
                            'Description': description,
                            'Low Price': low_price,
                            'High Price': high_price,
                            'Address': address,
                            'Latitude': latitude,
                            'Longitude': longitude,
                            'Brand Founding Date': brand_founding_date,
                        }
                        amenity_data = {f'Amenity_{amenity}': 1 if amenity in amenities else 0 for amenity in all_amenities}
                        apartment_data.update(amenity_data)
                        all_data.append(apartment_data)
                    except Exception as e:
                        logging.error(f"Error processing data for {url}: {e}")

            if all_data:
                if os.path.exists(OUTPUT_EXCEL_FILE):
                    df_existing = pd.read_excel(OUTPUT_EXCEL_FILE)
                    df_new = pd.DataFrame(all_data)
=======
                json_data = fetch_json_data(url, position)

                if isinstance(json_data, list):
                    apartment_data = process_apartment_data(json_data, position, url, all_amenities)
                elif isinstance(json_data, dict):
                    apartment_data = process_apartment_data([json_data], position, url, all_amenities)
                else:
                    return None
                
                if apartment_data is not None:
                    all_data.append(apartment_data)
                    logging.info(f"Successfully processed and appended data for position {position} — {url}")
                else:
                    logging.info(f"Failed to process data for position {position} — {url}")
            
            # Save data into Excel          
            if all_data:
                if os.path.exists(OUTPUT_EXCEL_FILE):
                    df_existing = pd.read_excel(OUTPUT_EXCEL_FILE)
                    df_new = pd.DataFrame(all_data).drop_duplicates()
>>>>>>> dev
                    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                    df_combined.to_excel(OUTPUT_EXCEL_FILE, index=False)
                else:
                    df_new = pd.DataFrame(all_data)
                    df_new.to_excel(OUTPUT_EXCEL_FILE, index=False)

            save_checkpoint(page_num)
            time.sleep(10)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    logging.info(f"Data extraction completed.")

if __name__ == "__main__":
    main()