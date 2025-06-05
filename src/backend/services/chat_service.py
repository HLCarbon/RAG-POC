# src/backend/chat_service.py

# Import necessary components
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chains import RetrievalQA
from .qdrant_vector_service import QdrantVectorService
from langchain.vectorstores.base import VectorStoreRetriever
import json

class ChatService:
    def __init__(self,
                 qdrant_vector_service: QdrantVectorService,
                 llm: BaseChatModel):
        """
        Initializes the ChatService with necessary components.

        Args:
            qdrant_vector_service: An initialized QdrantVectorService instance.
            llm: An initialized LLM instance.
        """
        self.qdrant_vector_service = qdrant_vector_service
        self.llm = llm
        self._qa_chain = self._initialize_qa_chain()

    def _initialize_qa_chain(self, chain_type: str = "stuff", search_kwargs: dict = None) -> RetrievalQA:
        """
        Creates and configures the Langchain RetrievalQA chain.

        Args:
            chain_type: The type of chain to use (e.g., "stuff", "map_reduce"). Defaults to "stuff".
            search_kwargs: Optional dictionary of keyword arguments for the retriever (e.g., {"k": 3}).

        Returns:
            A Langchain RetrievalQA instance.
        """
        if search_kwargs is None:
             search_kwargs = {"k": 3}
        retriever = self.qdrant_vector_service.get_retriever(search_kwargs=search_kwargs)

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=True
        )
        return qa_chain


    async def generate_response(self, query: str):
        """
        Generates a streaming response to a user query using the RAG pipeline.

        Args:
            query: The user's query string.

        Yields:
            Chunks of the generated response.

        Returns:
            The source documents related to the query.
        """
        # First, retrieve source documents based on the query
        retriever = self.qdrant_vector_service.get_retriever()
        source_documents = await retriever.ainvoke(query)

        # Prepare the prompt for the LLM, including retrieved context
        context = "\n\n".join([doc.page_content for doc in source_documents])
        full_prompt = f"Context: {context}\n\nQuestion: {query}"

        # Stream the response from the LLM
        response_generator = self.llm.astream(full_prompt)
        async for chunk in response_generator:
            yield chunk.content

        # After all chunks, yield the source documents as a JSON string
        # This allows the frontend to receive them as part of the stream
        yield "\nSOURCE_DOCUMENTS_START\n"
        yield json.dumps([{
            "page_content": doc.page_content,
            "metadata": doc.metadata
            } for doc in source_documents])
        yield "\nSOURCE_DOCUMENTS_END\n"