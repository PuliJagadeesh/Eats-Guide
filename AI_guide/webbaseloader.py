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


def download_photo(photo_reference, api_key, output_path, retries=3, delay=30):
    """
    Download and save a photo using the photo reference with retry logic.
    """
    url = f"https://maps.googleapis.com/maps/api/place/photo"
    params = {
        'photoreference': photo_reference,
        'key': api_key,
        'maxwidth': 400,  # Specify the image resolution
        'maxheight': 400
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, stream=True, timeout=10)
            if response.status_code == 200:
                with open(output_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Image saved to {output_path}")
                return True
            else:
                print(f"Failed to download image: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading photo (Attempt {attempt}/{retries}): {e}")

        # Wait before retrying
        if attempt < retries:
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    print(f"Failed to download image after {retries} attempts.")
    return False


def main():
    """
    Main script to process the input CSV, fetch place IDs, photo references, and download images.
    """
    # Load the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the CSV contains the required columns
    required_columns = ['Name', 'Location', 'Locality', 'City']
    for col in required_columns:
        if col not in df.columns:
            print(f"CSV file must contain the following columns: {', '.join(required_columns)}")
            return

    # Add a new column for image paths
    if 'Image_Path' not in df.columns:
        df['Image_Path'] = None

    # Get a list of existing image names in the output directory
    existing_images = {os.path.splitext(f)[0] for f in os.listdir(output_dir) if
                       os.path.isfile(os.path.join(output_dir, f))}

    # Iterate through each row in the CSV
    for index, row in df.iterrows():
        # Construct a sanitized image name
        name = row['Name']
        safe_name = "".join(c if c.isalnum() else "_" for c in name)

        # Skip if the image already exists in the directory
        if safe_name in existing_images:
            print(f"Image already exists for {row['Name']}, skipping...")
            continue

        # Construct a detailed search query
        location = row['Location']
        locality = row['Locality']
        city = row['City']
        query = f"{name}, {location}, {locality}, {city}"

        print(f"Processing: {query}")

        # Step 1: Get place_id
        place_id = get_place_id(query, API_KEY)
        if not place_id:
            continue

        # Step 2: Get photo_reference
        photo_reference = get_photo_reference(place_id, API_KEY)
        if not photo_reference:
            continue

        # Step 3: Download the photo
        output_path = os.path.join(output_dir, f"{safe_name}.jpg")

        if download_photo(photo_reference, API_KEY, output_path):
            # Update the DataFrame with the image path
            df.at[index, 'Image_Path'] = output_path

    # Save the updated DataFrame to a new CSV
    df.to_csv(output_csv, index=False)
    print(f"Updated CSV saved to {output_csv}")


if __name__ == "__main__":
    main()
