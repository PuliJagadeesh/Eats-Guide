import gradio as gr
from chromadblocal import DataHandler
from queryhandler import QueryHandler

# Initialize the DataHandler to access the ChromaDB collection and get unique cities
data_handler = DataHandler()
available_cities = data_handler.get_unique_cities()  # Get list of unique cities
# Initialize the QueryHandler with the ChromaDB collection
query_handler = QueryHandler(data_handler.get_collection())

# Function to handle user queries
def process_query(user_prompt):
    # Query the collection and return top results
    results = query_handler.query(user_prompt, n_results=5)

    # Generate the response based on the query results
    recommendation_text, image_paths = query_handler.generate_response(results, user_prompt)

    # Return response text and image paths (not gr.Image components)
    return recommendation_text, image_paths  # Return text and image paths

# Display greeting message along with available cities
def display_greeting_and_cities():
    greeting = ("Hi there! Got questions about restaurants, cuisines, locations, ratings, or costs in these cities?"
                " Just ask, and I’ll be thrilled to help you find what you need!")
    cities_list = ", ".join(available_cities)
    return f"{greeting}\n\nAvailable cities: {cities_list}"

# Create a Gradio interface
iface = gr.Interface(
    fn=process_query,  # Function to process input
    inputs=gr.Textbox(label="Ask about restaurants, cuisines, or more"),  # Custom label for input
    outputs=[
        gr.Textbox(label="Recommended Restaurants"),  # Text output for recommendations
        gr.Gallery(label="Restaurant Images")  # Gallery to display images
    ],
    title="Restaurant Query System",
    description=display_greeting_and_cities()  # Show greeting and cities above the input prompt
)

# Launch the Gradio app with allowed_paths specified
if __name__ == "__main__":
    iface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=True,
        allowed_paths=["D:/Projects/Liminal/AI_Guide/resources/uuid_images"]  # Specify allowed paths during launch
    )
