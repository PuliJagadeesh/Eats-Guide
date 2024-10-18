import pandas as pd

# Sample Data: Replace this with your actual DataFrame loading method
data = {
    'restaurant_name': [
        'Sabarees Veg Restaurant', 'Pechiamman Veg Restaurant', 'Hotel archanas',
        'Pechiamman Veg Restaurant', 'Hotel Shree Annapoorna Pure Veg', 'NammA AmmaN',
        'Shree Aishwaryam Pure Veg', 'Hotel Temple City Pure Veg', 'Gowri Parvathi Bhavan',
        'Modern Restaurant', 'Hotel Pranav', 'The Dessert Heaven - Pastry, Brownie and Cakes'
    ],
    'cuisine': [
        'South Indian, North Indian, Chinese, Biryani, Snacks, Beverages',
        'South Indian, North Indian, Chinese, Biryani, Snacks, Beverages',
        'South Indian', 'South Indian, North Indian, Chinese, Biryani, Snacks, Beverages',
        'Chinese, South Indian, North Indian, Snacks, Tandoor, Salads, Beverages',
        'South Indian, North Indian, Chinese, Biryani, Snacks, Beverages',
        'South Indian, Chinese, Biryani, Snacks, Beverages',
        'South Indian, North Indian, Chinese, Biryani, Snacks, Beverages',
        'South Indian, North Indian, Chinese', 'South Indian, North Indian, Chinese, Biryani, Snacks, Beverages',
        'South Indian, Chinese', 'Bakery, Desserts, Sweets, Ice Cream'
    ],
    'rating': [4.6, 4.4, 4.2, 4.5, 4.3, 4.4, 4.4, 4.3, 4.5, 4.7, 4.5, 4.5],
    'location': [
        'Southern Railway Colony', 'SS Colony', 'Southern Railway Colony',
        'SS Colony', 'SS Colony', 'Doak Nagar', 'Iyer Bungalow', 'Iyer Bungalow',
        'Opp to Sundaram Park', 'Periyar', 'Iyer Bungalow', 'Vidhya Colony'
    ],
    'description': [
        'ITEMS AT ₹79', 'PLACEHOLDER', '20% OFF UPTO ₹50', 'PLACEHOLDER',
        'ITEMS AT ₹79', '40% OFF UPTO ₹80', 'FREE ITEM', 'PLACEHOLDER',
        'PLACEHOLDER', 'ITEMS AT ₹99', '60% OFF UPTO ₹120', ''
    ],
    'image_url': [None] * 12  # Initialize with None or empty strings
}

# Create a DataFrame
df = pd.DataFrame(data)

# Fill missing values
# Instead of using inplace=True
df['cuisine'] = df['cuisine'].fillna('Not Available')
df['rating'] = df['rating'].fillna(0)
df['location'] = df['location'].fillna('Not Specified')
df['description'] = df['description'].replace('', 'No description available')


# Augment Image Links
base_image_url = "https://example.com/images/"  # Replace with your actual base URL
df['image_url'] = base_image_url + df['restaurant_name'].str.replace(' ', '_') + '.jpg'

# Display the updated DataFrame
print(df)
print(df.shape)
print(df.describe(include = 'all'))
print(df.isnull().sum().sum())

# Save the updated DataFrame to a new CSV file (optional)
df.to_csv('updated_restaurants.csv', index=False)

