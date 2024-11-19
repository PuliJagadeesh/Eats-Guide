from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from collections import deque

# Load environment variables from .env file
load_dotenv()


class QueryHandler:
    def __init__(self, collection, llm_model_name='llama-3.2-1b-preview',
                 embed_model_name='sentence-transformers/all-MiniLM-L6-v2', max_history=50):
        self.collection = collection
        self.embed_model = SentenceTransformer(embed_model_name)

        # Load the Groq API key from environment variable
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")

        # Initialize the LLM client with the API key
        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model_name=llm_model_name)

        # Session history management
        self.history = deque(maxlen=max_history)  # Store last 'max_history' interactions

    def query(self, user_prompt, n_results=5):
        query_embedding = self.embed_model.encode(user_prompt).tolist()

        # Perform the query in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def get_recent_context(self):
        # Retrieve recent history for context, including LLM-generated responses
        context_parts = []
        for idx, (prompt, results, llm_response) in enumerate(self.history):
            metadatas = results.get('metadatas', [])
            flat_metadatas = [item for sublist in metadatas for item in sublist]
            context = "\n".join(
                f"{idx + 1}. Restaurant: {metadata.get('restaurant_name', 'N/A')}, "
                f"Location: {metadata.get('location', 'N/A')}, "
                f"Locality: {metadata.get('locality', 'N/A')}, "
                f"City: {metadata.get('city', 'N/A')}, "
                f"Votes: {metadata.get('votes', 'N/A')}, "
                f"Cost: {metadata.get('cost', 'N/A')}, "
                f"Rating: {metadata.get('rating', 'N/A')}"
                for metadata in flat_metadatas
            )
            # Include the LLM-generated response for each entry
            context_parts.append(f"Query: {prompt}\nResults:\n{context}\nResponse:\n{llm_response}")

        return "\n".join(context_parts)

    def generate_response(self, results, user_prompt):
        # Gather recent context from history
        recent_context = self.get_recent_context()

        # Current query's results
        metadatas = results.get('metadatas', [])
        flat_metadatas = [item for sublist in metadatas for item in sublist]

        # Construct context from metadata
        context = "\n".join(
            f"Restaurant: {metadata.get('restaurant_name', 'N/A')}, "
            f"Location: {metadata.get('location', 'N/A')}, "
            f"Locality: {metadata.get('locality', 'N/A')}, "
            f"City: {metadata.get('city', 'N/A')}, "
            f"Votes: {metadata.get('votes', 'N/A')}, "
            f"Cost: {metadata.get('cost', 'N/A')}, "
            f"Rating: {metadata.get('rating', 'N/A')}"
            for metadata in flat_metadatas
        )

        # LLM prompt template with session context
        prompt_template = ChatPromptTemplate.from_template(
            """
            Previous Conversations:
            {recent_context}

            Here is the data relevant to your query:

            - **Name**: The restaurant's name.
            - **Location, Locality, and City**: The address details of the restaurant.
            - **Cuisine**: Types of cuisines offered by the restaurant.
            - **Rating**: Average rating on a scale of 5.
            - **Votes**: Number of people who have rated the restaurant.
            - **Cost**: Average cost of dining.

            You are a restaurant recommender with knowledge of restaurants, cuisines, ratings, and costs across various cities in India. Respond to queries based on the provided details and recommend the most relevant options based on user preferences. If information is incomplete, provide the best suggestions and encourage follow-up questions.

            When generating responses:

            - Respond directly with restaurant recommendations and relevant details.
            - Sort the recommendations by relevance, based on the following strategy:

              **Relevance Strategy**:
              Order restaurants using a calculated relevance score to determine the best fit based on user preferences:
              - **Cuisine Match**: Prioritize restaurants that match the specified cuisine, if mentioned.
              - **Rating**: Higher ratings contribute to relevance, favoring restaurants with 4.0+ ratings.
              - **Votes**: Restaurants with more votes gain slightly higher relevance to reflect popularity.
              - **Cost Match**: Prefer restaurants within the user’s specified budget or the closest match.
              Each restaurant is evaluated on these criteria, with higher weighting given to direct matches on cuisine, budget, and rating.

            Do not calculate or show relevance scores directly to the user. Instead, use this strategy to sort restaurants in descending order of relevance.
            Use the recent context only if you require additional information from previous conversation. 
            If the query is not related to the information available to you, make a generic response and let the user know you would be more than happy to help with restaurant recommendations

            <context>
            {context}
            </context>
            Question: {input}
            """
        )

        # Generate the prompt by formatting the template
        prompt = prompt_template.format(recent_context=recent_context, context=context, input=user_prompt)

        # Use the LLM to generate the output
        response = self.llm.invoke(prompt)  # Pass the prompt string directly

        # Store the prompt, results, and LLM-generated response in the history
        self.history.append((user_prompt, results, response.content))

        return response.content  # Adjust this line to match the actual attribute of the response
