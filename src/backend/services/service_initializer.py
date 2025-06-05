import dotenv
import os
from qdrant_client import QdrantClient
from document_processing.document_processor import DocumentProcessor
from .azure_llm_service import AzureLLMService
from .data_ingestion_service import DataIngestionService
from .qdrant_vector_service import QdrantVectorService
from .chat_service import ChatService
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel

dotenv.load_dotenv()


def initialize_services():
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
    PDF_DATA_PATH = os.getenv("PDF_DATA_PATH")
    VECTOR_SIZE = int(os.getenv("VECTOR_SIZE"))

    if not QDRANT_URL or not QDRANT_PORT:
        raise ValueError("QDRANT_URL and QDRANT_PORT environment variables must be set.")

    client = QdrantClient(url=QDRANT_URL, port=QDRANT_PORT)

    if not PDF_DATA_PATH:
         raise ValueError("PDF_DATA_PATH environment variable must be set and point to your PDF document.")
    document_processor = DocumentProcessor(data_path=PDF_DATA_PATH)

    azure_llm_service = AzureLLMService(VECTOR_SIZE)
    embeddings: Embeddings = azure_llm_service.get_embeddings()
    llm: BaseChatModel = azure_llm_service.get_llm()

    if not QDRANT_COLLECTION_NAME:
        raise ValueError("QDRANT_COLLECTION_NAME environment variable must be set.")

    qdrant_vector_service = QdrantVectorService(
        client=client,
        embeddings=embeddings,
        collection_name=QDRANT_COLLECTION_NAME,
        vector_size=VECTOR_SIZE
    )

    data_ingestion_service = DataIngestionService(
        vector_store=qdrant_vector_service.get_vector_store(),
        document_processor=document_processor,
        collection_name=QDRANT_COLLECTION_NAME,
    )

    chat_service = ChatService(
        qdrant_vector_service=qdrant_vector_service,
        llm=llm
    )

    return {
        "data_ingestion_service": data_ingestion_service,
        "chat_service": chat_service
    } 