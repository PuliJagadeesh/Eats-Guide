#from datahandler import DataHandler
from chromadblocal import DataHandler
from queryhandler import QueryHandler

# Main function to coordinate the process
def main():
    # Initialize the DataHandler with local ChromaDB hosting
    data_handler = DataHandler()

    # Load the CSV data from the specified path
    df = data_handler.load_data("D:/Projects/Liminal/app/AI_guide/restaurants.csv")

    # Process the data and store embeddings in the local ChromaDB instance
    data_handler.process_data(df)  # Ensure embeddings are stored in ChromaDB

    # Initialize the QueryHandler with the ChromaDB collection from DataHandler
    query_handler = QueryHandler(data_handler.get_collection())

    # Ask the user to input their query via the terminal
    user_prompt = input("Enter your query: ")

    # Query the collection and return top 5 results
    results = query_handler.query(user_prompt, n_results=5)

    # Display the results to the user
    query_handler.display_results(results)

# Ensure the main function runs when this script is executed
if __name__ == "__main__":
    main()
