import os
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables from .env file
load_dotenv()


class QueryHandler:
    def __init__(self, retriever, llm_model_name='llama-3.2-1b-preview',
                 embed_model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.retriever = retriever
        self.embed_model = SentenceTransformer(embed_model_name)

        # Load the Groq API key from environment variable
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")

        # Initialize the LLM client with the API key
        self.llm = ChatGroq(groq_api_key=self.groq_api_key, model_name=llm_model_name)

    def query(self, user_prompt, n_results=5):
        # Invoke the retriever to get results based on user prompt
        response = self.retriever.invoke(user_prompt)
        return response

    def generate_response(self, results, user_prompt):
        if not results:
            return "I don't know."

        # Construct context from the retrieved data
        context = "\n".join(
            f"Title: {item.metadata.get('title', 'N/A')}, "
            f"Source: {item.metadata.get('source', 'N/A')}, "
            f"Score: {item.metadata.get('score', 'N/A')}"
            for item in results
        )

        # LLM prompt template
        prompt_template = ChatPromptTemplate.from_template(
            """
            Firstly, understand the question. Then using the retrieved information, generate a relevant response
            for the user prompt, and attach the source link with the generated response. 

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
        if not results:
            print("No results found.")
            return

        for item in results:
            print(f"Title: {item.metadata.get('title', 'N/A')}")
            print(f"Source: {item.metadata.get('source', 'N/A')}")
            print(f"Score: {item.metadata.get('score', 'N/A')}")
            print("-" * 40)


# Main execution
if __name__ == "__main__":
    # Initialize the retriever
    os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
    retriever = TavilySearchAPIRetriever(k=5, verbose=True)

    # Create an instance of QueryHandler
    query_handler = QueryHandler(retriever)

    # Continuous loop for user queries
    while True:
        user_prompt = input("Enter your query (or type 'exit' to terminate): ")

        if user_prompt.lower() == 'exit':
            print("Terminating the program.")
            break

        # Perform the query and retrieve results
        results = query_handler.query(user_prompt)

        # Display results and generate response
        #query_handler.display_results(results)
        generated_response = query_handler.generate_response(results, user_prompt)
        print("\nLLM Response:", generated_response)
