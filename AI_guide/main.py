import gradio as gr
from chromadblocal import DataHandler
from queryhandler import QueryHandler

# Function to handle user queries
def process_query(user_prompt):
    # Initialize the DataHandler to access the ChromaDB collection
    data_handler = DataHandler()

    # Initialize the QueryHandler with the ChromaDB collection
    query_handler = QueryHandler(data_handler.get_collection())

    # Query the collection and return top results
    results = query_handler.query(user_prompt, n_results=5)

    # Generate the response based on the query results
    response = query_handler.generate_response(results, user_prompt)
    return response

# Create a Gradio interface
iface = gr.Interface(
    fn=process_query,  # Function to process input
    inputs="text",     # Input type (text field)
    outputs="text",    # Output type (text response)
    title="Restaurant Query System"
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860, share=True)

