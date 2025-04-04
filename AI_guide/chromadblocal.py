import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

class DataHandler:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2', db_path="D:/Projects/Liminal/AI_guide/AI_guide/chromadb_img"):
        # Initialize the ChromaDB persistent client and embedding model
        self.client = chromadb.PersistentClient(path=db_path)  # ChromaDB with persistent storage at the specified path
        self.model = SentenceTransformer(model_name)
        self.collection = self.client.get_or_create_collection(name="food_places")

    def load_data(self, file_path):
        """
        Load data from a CSV file.
        :param file_path: Path to the CSV file.
        :return: DataFrame with loaded data.
        """
        return pd.read_csv(file_path)

    def get_unique_cities(self):
        """
        Retrieve unique cities from the restaurant dataset.
        :return: List of unique cities.
        """
        df = self.load_data("D:/Projects/Liminal/AI_Guide/resources/restaurant_uuid_images.csv")
        return sorted(df['City'].unique().tolist())
    def process_data(self, df):
        """
        Preprocess the DataFrame and generate text embeddings for each row.
        :param df: DataFrame containing restaurant data.
        """
        count = 0
        for idx, row in df.iterrows():

            combined_text = f"{row['Cuisine']} {row['Location']} {row['Locality']} {row['Cost']}"
            embedding = self.model.encode(combined_text).tolist()

            # Create new metadata for each row
            new_metadata = {
                "restaurant_name": row['Name'],
                "location": row['Location'],
                "locality": row['Locality'],
                "city": row['City'],
                "votes": row['Votes'],
                "cost": row['Cost'],
                "rating": row['Rating'],
                "uuid": row['Unique_ID'],
                "image_path": row['Image_Path']
            }

            # Check if the ID already exists in the collection
            existing_docs = self.collection.get(ids=[str(idx)])  # Fetch existing document by ID

            if existing_docs['ids']:  # If the ID exists
                # Check if the metadata is the same
                existing_metadata = existing_docs['metadatas'][0]  # Get the existing metadata for comparison
                if existing_metadata == new_metadata:
                    continue  # Skip if metadata is the same

            # Insert or update the collection
            self.collection.add(
                documents=[combined_text],  # Add text for reference
                metadatas=[new_metadata],   # Use the new_metadata created before the condition
                embeddings=[embedding],
                ids=[str(idx)]  # Use index as ID
            )
            count = count+1
            if count%10 == 0:
                print(f"Inserted/Updated {count} rows into ChromaDB.")

    def get_collection(self):
        return self.collection  # Return the ChromaDB collection instance

# If you want to run this file separately to update the vector DB
if __name__ == "__main__":
    data_handler = DataHandler()
    df = data_handler.load_data("D:/Projects/Liminal/AI_Guide/resources/restaurant_uuid_images.csv")
    data_handler.process_data(df)