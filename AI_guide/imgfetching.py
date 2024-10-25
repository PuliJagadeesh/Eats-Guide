import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Function to fetch image URL from Google Images (or another source)
def fetch_image_url(restaurant_name, location, city):
    query = f"{restaurant_name} {location} {city} restaurant image"
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image elements in the page
    images = soup.find_all('img')

    # Check each image for a valid 'src' attribute (only HTTP URLs, not base64 images)
    for img in images:
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            # Return the first valid image URL
            return img_url

    # Return None if no valid image is found
    return None

# Main function to process the dataset and fetch image URLs
def process_csv_and_fetch_images(csv_file_path, output_folder):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    count = 0

    # Add a new column for the image URL if it doesn't exist
    if 'image_url' not in df.columns:
        df['image_url'] = None

    # Loop through each row in the dataset
    for index, row in df.iterrows():
        restaurant_name = row['Name']
        location = row['Location']
        city = row['City']

        # Fetch the image URL
        image_url = fetch_image_url(restaurant_name, location, city)
        if image_url:
            # Update the 'image_url' column with the image URL
            df.at[index, 'image_url'] = image_url
            count += 1

        # Logging progress every 1000 records processed
        if count % 1000 == 0:
            print(f"Processed {count} valid image URLs so far...")

    # Save the updated CSV with image URLs
    updated_csv_path = os.path.join(resource_folder, "restaurants_with_images.csv")
    df.to_csv(updated_csv_path, index=False)
    print(f"Updated CSV saved: {updated_csv_path}")
    print(f"Total of {count} records saved in the dataframe")


# Example usage
csv_file_path = "D:/Projects/Liminal/AI_Guide/resources/restaurants_1.csv"  # Replace with your actual CSV file path
output_folder = "D:/Projects/Liminal/AI_Guide/resources/images"  # Replace with your desired output folder path for images
resource_folder = "D:/Projects/Liminal/AI_Guide/resources"

process_csv_and_fetch_images(csv_file_path, output_folder)
