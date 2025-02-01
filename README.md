## **EatsGuide - Taste, Explore, Enjoy**

**An AI-powered restaurant recommendation system using LLMs, ChromaDB, and advanced filtering techniques.**

This project enhances restaurant recommendations by integrating **large language models (LLMs)** with **vector databases (ChromaDB)** to provide context-aware responses. By leveraging embeddings, natural language understanding, and retrieval-augmented generation (RAG), the system delivers highly relevant restaurant suggestions based on user queries.

---

## **Project Overview**

### **Architecture**
![Project Architecture](resources/proposed_arch1.jpeg)

### **Features & Enhancements**
- **ChromaDB for Efficient Retrieval**: Stores restaurant data as embeddings for fast and relevant search results.
- **LLM-Powered Query Processing**: Uses **Llama 3.3-70B** to extract and process user intent.
- **Advanced Query Filtering**: Identifies cuisine, location, and price filters from user queries using an LLM-based extraction mechanism.
- **Session-Based Context Management**: Maintains conversational context to provide more coherent and refined recommendations.
- **Gradio-Based Interactive UI**: A user-friendly interface for querying and exploring recommendations.
- **Restaurant Image Display**: Returns restaurant images along with textual recommendations.

---

## **Implementation Details**

### **Query Handling with ChromaDB & LLMs**
1. **User Input Processing**: The system receives a user query through a Gradio UI.
2. **Filter Extraction**: The LLM extracts restaurant attributes such as cuisine, location, and budget from the query.
3. **Vector Search in ChromaDB**: The extracted filters and query embeddings are used to retrieve the most relevant results.
4. **Response Generation with Context Awareness**:
   - The system maintains conversation history using a session-based deque structure.
   - It constructs a detailed response based on retrieved restaurant metadata and previous interactions.
5. **Returning Recommendations**:
   - The generated text response is displayed in the Gradio UI.
   - Associated restaurant images are retrieved and presented in a gallery format.

---

## **System Components**
### **Data Processing & Storage**
- **ChromaDB**: Stores restaurant data embeddings and facilitates efficient search.
- **Sentence Transformers**: Generates embeddings for user queries and database entries.

### **AI & NLP Modules**
- **LLM (Llama 3.3-70B)**: Extracts intent, applies filters, and generates responses.
- **ChatGroq API**: Facilitates LLM-based query interpretation and response synthesis.

### **User Interface**
- **Gradio**: Provides an intuitive UI for users to interact with the system.
- **Dynamic Greeting Display**: Lists available cities based on stored restaurant data.

---

## **How to Run the Project**
### **Setup & Requirements**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/EatsGuide.git
   cd EatsGuide
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up API Keys:**
   - Create a `.env` file and add your **GROQ_API_KEY**:
     ```plaintext
     GROQ_API_KEY=your_api_key_here
     ```
4. **Run the Application:**
   ```bash
   python app.py
   ```
5. **Access the Gradio Interface:**
   - Open `http://127.0.0.1:7860` in your browser.

---

## **Future Improvements**
- **Enhanced Personalization**: Improve recommendations based on user preferences and feedback.
- **Multimodal Search**: Support voice and image-based queries.
- **Expanded Coverage**: Integrate more cities and cuisines for a broader restaurant database.

---

## **Contributors**
- **Dhanvanth Voona** - [LinkedIn](https://www.linkedin.com/in/dhanvanth-voona/) | [GitHub](https://github.com/dhanvanthvoona)

---

EatsGuide is an evolving AI project designed to simplify restaurant discovery with intelligent recommendations. Enjoy exploring and discovering great food!

