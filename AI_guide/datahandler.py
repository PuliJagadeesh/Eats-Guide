import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb



class DataHandler:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        # Initialize the ChromaDB client and embedding model
        self.client = chromadb.Client()
        self.model = SentenceTransformer(model_name)
        self.collection = self.client.create_collection(name="food_places")

    def load_data(self, file_path):
        """
        Load data from a CSV file.
        :param file_path: Path to the CSV file.
        :return: DataFrame with loaded data.
        """
        return pd.read_csv(file_path)

    def process_data(self, df):

        # Generate embeddings and store in ChromaDB
        for idx, row in df.iterrows():
            combined_text = f"{row['description']} {row['cuisine']} {row['location']}"
            embedding = self.model.encode(combined_text).tolist()

            # Insert data into ChromaDB
            self.collection.add(
                documents=[combined_text],  # Add text for reference
                metadatas=[{
                    "restaurant_name": row['restaurant_name'],
                    "location": row['location'],
                    "rating": row['rating'],
                    "image_url": row['image_url']
                }],
                embeddings=[embedding],
                ids=[str(idx)]  # Use index as ID
            )

        print(f"Inserted {len(df)} records into ChromaDB.")

    def get_collection(self):
        return self.collection
