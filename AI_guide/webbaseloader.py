import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Your Google API Key
API_KEY = os.getenv('PLACES_API_KEY')

# File paths
input_csv = "D:/Projects/Liminal/AI_Guide/resources/restaurants_1.csv"  # Input CSV file
output_dir = 'D:/Projects/Liminal/AI_Guide/resources/restaurant_images'  # Directory to save images
PHOTO_BASE_URL = "https://maps.googleapis.com/maps/api/place/photo"
output_csv = "D:/Projects/Liminal/AI_Guide/resources/output.csv"
# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def get_place_id(query, api_key):
    """
    Search for a place using Google Places API and return the place_id.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK' and len(data['results']) > 0:
        return data['results'][0]['place_id']
    else:
        print(f"Place not found for query: {query}")
        return None

def get_photo_reference(place_id, api_key):
    """
    Get the photo reference for a place using its place_id.
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'OK' and 'photos' in data['result']:
        return data['result']['photos'][0]['photo_reference']
    else:
        print(f"No photos found for place_id: {place_id}")
        return None

def download_photo(photo_reference, api_key, output_path):
    """
    Download and save a photo using the photo reference.
    """
    url = f"https://maps.googleapis.com/maps/api/place/photo"
    params = {
        'maxwidth': 400,  # Specify the image resolution (can also use maxheight)
        'maxheight': 400,
        'photo_reference': photo_reference,  # Use the exact parameter name
        'key': api_key
    }
    response = requests.get(url, params=params, stream=True)

    # Ensure the response is successful
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image saved to {output_path}")
    else:
        print(f"Failed to download image: {response.status_code} - {response.text}")

def main():
    """
    Main script to process the input CSV, fetch place IDs, photo references, download images,
    and save the image paths in the dataframe.
    """
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the CSV contains the required columns
    required_columns = ['Name', 'Location', 'Locality', 'City']
    for col in required_columns:
        if col not in df.columns:
            print(f"CSV file must contain the following columns: {', '.join(required_columns)}")
            return

    # Create a new column for image paths
    df['Image_Path'] = None

    # Iterate through each row in the CSV
    for index, row in df.iterrows():
        # Construct a detailed search query
        name = row['Name']
        location = row['Location']
        locality = row['Locality']
        city = row['City']
        query = f"{name}, {location}, {locality}, {city}"

        print(f"Processing: {query}")

        # Step 1: Get place_id
        place_id = get_place_id(query, API_KEY)
        if not place_id:
            print(f"Skipping: Could not find place ID for {query}")
            continue

        # Step 2: Get photo_reference
        photo_reference = get_photo_reference(place_id, API_KEY)
        if not photo_reference:
            print(f"Skipping: Could not find photo reference for {query}")
            continue

        # Step 3: Download the photo
        safe_name = "".join(c if c.isalnum() else "_" for c in name)  # Sanitize the filename
        output_path = os.path.join(output_dir, f"{safe_name}.jpg")
        download_photo(photo_reference, API_KEY, output_path)

        # Step 4: Save the output path in the dataframe
        df.at[index, 'Image_Path'] = output_path

    # Save the updated dataframe to a new CSV file
    #output_csv = os.path.join(output_dir, "output.csv")
    df.to_csv(output_csv, index=False)
    print(f"Updated dataframe saved to {output_csv}")

if __name__ == "__main__":
    main()
