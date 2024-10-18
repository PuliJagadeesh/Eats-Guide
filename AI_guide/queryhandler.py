from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class QueryHandler:
    def __init__(self, collection, llm_model_name='llama-3.2-1b-preview', embed_model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.collection = collection
        self.embed_model = SentenceTransformer(embed_model_name)

        # Load the Groq API key from environment variable
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")

        # Initialize the LLM client with the API key
        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model_name=llm_model_name)

    def query(self, user_prompt, n_results=5):
        query_embedding = self.embed_model.encode(user_prompt).tolist()

        # Perform the query in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def generate_response(self, results, user_prompt):
        metadatas = results.get('metadatas', [])
        if not metadatas:
            return "I don't know."

        # Construct context from metadata
        context = "\n".join(
            f"Restaurant: {metadata.get('restaurant_name', 'N/A')}, Location: {metadata.get('location', 'N/A')}, Rating: {metadata.get('rating', 'N/A')}, Image URL: {metadata.get('image_url', 'N/A')}"
            for metadata in metadatas[0]  # Take the first batch of results
        )

        # LLM prompt template
        prompt_template = ChatPromptTemplate.from_template(
            """
            Firstly understand the question, if the question is not relevant to the retrieved data
            tell the user that you do not have sufficient information about the given question.
            And if the question is relevant to retrieved data, then generate the response from the 
            retrieved data, and you do not have to access the image urls, you can just give the related
            urls along with their meta data. 
            
            <context>
            {context}
            </context>
            Question: {input}
            """
        )

        # Generate the prompt by formatting the template
        prompt = prompt_template.format(context=context, input=user_prompt)

        # Use the LLM to generate the output
        response = self.llm.invoke(prompt)  # Pass the prompt string directly

        # Access the content of the response (assuming it's an AIMessage object)
        return response.content  # Adjust this line to match the actual attribute of the response

    def display_results(self, results):
        # Display query results
        print("Results structure:", results)  # Debugging line to check structure
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
