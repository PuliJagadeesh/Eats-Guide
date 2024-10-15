from sentence_transformers import SentenceTransformer


class QueryHandler:
    def __init__(self, collection, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize QueryHandler with the collection and model.
        :param collection: The ChromaDB collection to query.
        :param model_name: The pre-trained model name for embedding generation.
        """
        self.collection = collection
        self.model = SentenceTransformer(model_name)

    def query(self, user_prompt, n_results=5):
        """
        Query the collection using a user prompt and return top-k results.
        :param user_prompt: The user input prompt.
        :param n_results: Number of top results to return.
        :return: List of top-k results from ChromaDB.
        """
        query_embedding = self.model.encode(user_prompt).tolist()

        # Perform the query in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def display_results(self, results):
        """
        Display the query results.
        :param results: List of query results from ChromaDB.
        """
        print("Results structure:", results)  # Debugging line to check structure

        # Loop through the 'metadatas' field in the results
        metadatas = results.get('metadatas', [])
        if not metadatas:
            print("No metadata found.")
            return

        for metadata_list in metadatas:  # 'metadatas' is a list of lists
            for metadata in metadata_list:
                if isinstance(metadata, dict):
                    print(f"Restaurant: {metadata.get('restaurant_name', 'N/A')}")
                    print(f"Location: {metadata.get('location', 'N/A')}")
                    print(f"Rating: {metadata.get('rating', 'N/A')}")
                    print(f"Image URL: {metadata.get('image_url', 'N/A')}")
                    print("-" * 40)
                else:
                    print("Unexpected result format:", metadata)

# Example usage:
# Assume `collection` is your ChromaDB collection.
# handler = QueryHandler(collection)
# results = handler.query("Best places to eat in Jaipur")
# handler.display_results(results)
