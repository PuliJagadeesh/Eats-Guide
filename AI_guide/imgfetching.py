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

    images = soup.find_all('img')
    # Check each image for a valid 'src' attribute
    for img in images:
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):  # Only return valid URLs (filter out base64-encoded images)
            return img_url

    return None  # Return None if no valid image is found


# Function to download image from a URL
def download_image(image_url, restaurant_name, folder_path):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Make sure the folder exists
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Create a valid filename by replacing spaces with underscores
            image_name = restaurant_name.replace(" ", "_") + ".jpg"
            image_path = os.path.join(folder_path, image_name)

            # Write image to folder
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"Image saved: {image_path}")
            return image_path
        else:
            print(f"Failed to retrieve image for {restaurant_name}")
            return None
    except Exception as e:
        print(f"Error downloading image for {restaurant_name}: {e}")
        return None


# Main function to process the dataset
def process_csv_and_download_images(csv_file_path, output_folder):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    count = 0

    # Add a new column for the image URL
    df['image_url'] = None

    # Loop through each row in the dataset
    for index, row in df.iterrows():
        restaurant_name = row['Name']
        location = row['Location']
        city = row['City']

        # Fetch the image URL
        image_url = fetch_image_url(restaurant_name, location, city)
        if image_url:
            # Download the image and get the local path
            image_path = download_image(image_url, restaurant_name, output_folder)

            # Update the 'image_url' column with the image URL
            df.at[index, 'image_url'] = image_url
            count += 1

    # Save the updated CSV with image URLs
    updated_csv_path = os.path.join(resource_folder, "restaurants_with_images.csv")
    df.to_csv(updated_csv_path, index=False)
    print(f"Updated CSV saved: {updated_csv_path}")
    print(f"Total of {count} records saved in the dataframe")


# Example usage
csv_file_path = "D:/Projects/Liminal/AI_Guide/resources/restaurants_1.csv"  # Replace with your actual CSV file path
output_folder = "D:/Projects/Liminal/AI_Guide/resources/images"  # Replace with your desired output folder path for images
resource_folder = "D:/Projects/Liminal/AI_Guide/resources"

process_csv_and_download_images(csv_file_path, output_folder)
