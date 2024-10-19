from chromadblocal import DataHandler
from queryhandler import QueryHandler

# Main function to coordinate the process
def main():
    # Initialize the DataHandler with local ChromaDB hosting
    data_handler = DataHandler()

    # Load the CSV data from the specified path
    df = data_handler.load_data("D:/Projects/Liminal/AI_guide/resources/restaurants.csv")

    # Process the data and store embeddings in the local ChromaDB instance
    data_handler.process_data(df)

    # Initialize the QueryHandler with the ChromaDB collection from DataHandler
    query_handler = QueryHandler(data_handler.get_collection())

    while True:
        # Ask the user to input their query via the terminal
        user_prompt = input("Enter your query (or type 'exit' to terminate): ")

        if user_prompt.lower() == 'exit':
            print("Exiting the program.")
            break

        # Query the collection and return top results
        results = query_handler.query(user_prompt, n_results=5)

        # Generate the response based on the query results
        response = query_handler.generate_response(results, user_prompt)
        print("Response:", response)

# Ensure the main function runs when this script is executed
if __name__ == "__main__":
    main()
