import pandas as pd
import os

# Load the CSV file
file_path = "D:/Projects/Liminal/AI_Guide/resources/Dataset.csv"  # Update with your input CSV file path
df = pd.read_csv(file_path)

# Define S3 bucket details
bucket_name = "restaurant-resources-liminal"
region = "ap-south-1"
s3_base_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/uuid_images/"

# Update the Image_path column with S3 URLs using the Unique_ID column
df['S3Image_path'] = df['Unique_ID'].apply(lambda x: f"{s3_base_url}{x}.png")

# Save the updated DataFrame back to a new CSV file
#updated_csv_path = "updated_restaurant_data.csv"
#df.to_csv(updated_csv_path, index=False)

#print(f"Updated CSV file saved to: {updated_csv_path}")
"""
# Function to extract the file type and build S3 URL
def generate_s3_url(image_path, unique_id):
    # Extract file extension dynamically
    file_extension = os.path.splitext(image_path)[-1]  # E.g., '.jpg', '.png'
    # Build the full S3 URL
    return f"{s3_base_url}{unique_id}{file_extension}"""

# Apply the function to create a new 'S3_Image_URL' column
#df['S3_Image_URL'] = df.apply(lambda row: generate_s3_url(row['Image_path'], row['Unique_ID']), axis=1)

# Save the updated DataFrame to a new CSV
output_file_path = 'D:/Projects/Liminal/AI_Guide/resources/S3Dataset.csv'
df.to_csv(output_file_path, index=False)

print(f"Updated CSV file saved at: {output_file_path}")
