from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_qdrant import QdrantVectorStore
from langchain.vectorstores.base import VectorStoreRetriever


class QdrantVectorService:
    def __init__(self,
                 client: QdrantClient,
                 embeddings: Embeddings,
                 collection_name: str,
                 vector_size: int):
        """
        Initializes the QdrantVectorService.

        Args:
            client: An initialized QdrantClient instance.
            embeddings: An initialized embeddings instance.
            collection_name: The name of the Qdrant collection.
            vector_size: The dimension of the vectors to be stored.
        """
        self.client = client
        self.embeddings = embeddings
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._check_if_collection_exists()

        # Initialize Qdrant as a Langchain VectorStore instance
        self._vstore: VectorStore = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
    
    def get_vector_store(self):
        return self._vstore
    
    def get_retriever(self, search_kwargs: dict = None) -> VectorStoreRetriever:
        """
        Gets a configured Langchain retriever instance.

        Args:
            search_kwargs: Optional dictionary of keyword arguments for the retriever (e.g., {"k": 3}).

        Returns:
            A Langchain VectorStoreRetriever instance.
        """
        # Create and return a retriever from the vector store
        if search_kwargs is None:
            search_kwargs = {}
        return self._vstore.as_retriever(search_kwargs=search_kwargs)
    
    def _check_if_collection_exists(self):
        # Check if collection exists, create if not
        if not self.client.collection_exists(collection_name=self.collection_name):
            print(f"Collection '{self.collection_name}' not found. Creating...")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            print(f"Collection '{self.collection_name}' created.")