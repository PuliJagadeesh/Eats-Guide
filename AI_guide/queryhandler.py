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
                 embed_model_name='sentence-transformers/all-MiniLM-L6-v2', max_history=5):
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

        # Store the prompt and result in the history
        self.history.append((user_prompt, results))

        return results

    def get_recent_context(self):
        # Retrieve recent history for context, format it as a string
        context_parts = []
        for idx, (prompt, results) in enumerate(self.history):
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
            context_parts.append(f"Query: {prompt}\nResults:\n{context}")

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
            - Sort the recommendations by relevance, based on a calculated **Relevance Score** (details below), without showing the calculations to the user.

            **Relevance Score Calculation**:
            The Relevance Score is calculated as follows:

            Relevance Score = (Rating / 5) * W1 + log(1 + Votes) * W2 + (1 / Cost) * W3

            where:
            - **Rating** is the restaurant's rating out of 5.
            - **Votes** is the number of ratings for the restaurant.
            - **Cost** is the average cost per person.
            - **W1, W2, and W3** are weights. Set W1 = W2 = W3 = 1 for this calculation.

            **Sort** the list of restaurants in descending order of their Relevance Score, placing the most relevant recommendation at the top. Do not show any calculations or mention the Relevance Score directly in the response.

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

        return response.content  # Adjust this line to match the actual attribute of the response
