# RAG Proof-of-Concept Application

This project demonstrates a simple Retrieval-Augmented Generation (RAG) application. It allows you to chat with a PDF document, leveraging a combination of a FastAPI backend, a simple HTML/CSS/JS frontend, and a Qdrant vector database, all orchestrated with Docker Compose.

## How It Works

The application is structured into three main services:

1.  **Backend (FastAPI)**: Built with Python, FastAPI, Langchain, and Langgraph. It handles:
    *   Checking the status of the Qdrant vector database.
    *   Processing a PDF document: loading, splitting its text into chunks, embedding these chunks into vector representations, and storing them in Qdrant.
    *   Responding to user queries: It performs a similarity search in Qdrant to retrieve relevant document chunks based on the user's question, then passes these chunks along with the query to a Language Model (LLM) to generate a coherent answer.

2.  **Frontend (HTML/CSS/JS)**: A lightweight web interface that provides:
    *   A chat interface for user interaction.
    *   Displays messages from the user and the RAG bot.
    *   Notifies the user about the document processing status.
    *   Communicates with the backend using standard web requests.

3.  **Qdrant Vector Database**: A high-performance vector similarity search engine used to store and retrieve the embedded document chunks efficiently. It's configured with a named Docker volume for data persistence.

### Workflow Overview

1.  Upon launching the application and loading the frontend, it checks if the PDF data is already processed in Qdrant.
2.  If the data is not found, the backend automatically processes the PDF document, converting it into embeddings and storing them in Qdrant.
3.  Once the document is processed, users can type questions into the chat interface.
4.  The frontend sends the query to the backend, which then retrieves relevant information from Qdrant and uses an LLM to formulate a response.
5.  The LLM's response is displayed in the chat interface.

## Technologies Used

*   **Backend**: Python, FastAPI, Langchain, Langgraph, `qdrant-client`.
*   **Frontend**: HTML, CSS, JavaScript.
*   **Database**: Qdrant (Vector Database).
*   **Containerization**: Docker, Docker Compose.
*   **Document Handling**: PDF (for the source document).
*   **LLM Integration**: Via Langchain, allowing flexibility in choosing your preferred Large Language Model.

## How to Run It Yourself

To get this application up and running on your local machine, follow these steps:

1.  **Prerequisites**:
    *   Ensure you have Docker and Docker Compose installed on your system. You can download them from [Docker's official website](https://www.docker.com/get-started).
    *   A PDF document (e.g., a book or a technical paper) you wish to use for RAG. Place this file in the `data/` directory (you might need to create this directory).

2.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd RAG
    ```

3.  **Place Your PDF**: Place your PDF document (e.g., `my_book.pdf`) inside the `data/` directory.

4.  **Configure Environment Variables**:
    Following the example of `src/.env.example`, add the necessary env variables to be able to run the app.

5.  **Build and Run with Docker Compose**:
    Navigate to the root directory of the project (where `docker-compose.yml` is located) and run:
    ```bash
    docker compose up 
6.  **Access the Application**:
    *   Once the services are up and running, open your web browser and go to `http://localhost:8000` (or the port configured for your frontend service in `docker-compose.yml`).
    *   The frontend will automatically check for processed data. If not found, it will trigger the backend to process your PDF. This might take some time depending on the document size.

7.  **Start Chatting**:
    *   After the document processing is complete (indicated by frontend notifications), you can start typing your questions into the chat interface.

## How It Can Be Changed for Your Needs

This project is designed to be a flexible proof-of-concept. Here are several ways you can modify it to suit your specific requirements:

*   **Change the LLM**: The backend uses Langchain, which supports integration with various LLMs (e.g., OpenAI GPT, Google Gemini, Anthropic Claude, Hugging Face models, local Ollama models). You can easily switch the LLM by modifying the Langchain integration in the backend code.

*   **Integrate Different Data Sources**: Instead of a PDF, you could adapt the backend to ingest data from:
    *   Web pages (using Langchain's web loaders).
    *   Databases.
    *   APIs.
    *   Other document formats (e.g., DOCX, Markdown, plain text).

*   **Enhance Frontend UI/UX**: The frontend is a basic HTML/CSS/JS application. You can:
    *   Redesign the chat interface for a more modern look and feel.
    *   Implement real-time updates using WebSockets instead of polling for document processing status.
    *   Add advanced features like chat history, user authentication, or file upload interfaces.
    *   Integrate a JavaScript framework like React, Vue, or Angular for a more robust frontend.

*   **Advanced RAG Techniques**: Explore more sophisticated RAG patterns using Langgraph, such as:
    *   Multi-hop reasoning.
    *   Self-correction.
    *   Agentic workflows.

Feel free to explore the codebase and adapt it to your specific RAG use cases! 