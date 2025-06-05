from langchain_qdrant import QdrantVectorStore
from document_processing.document_processor import DocumentProcessor

class DataIngestionService:
    def __init__(self,
                 vector_store: QdrantVectorStore,
                 document_processor: DocumentProcessor,
                 collection_name: str,
                 ):
        """
        Initializes the DataIngestionService with necessary components.

        Args:
            vector_store: An initialized QdrantClient instance.
            document_processor: An initialized DocumentProcessor instance.
            collection_name: The name of the Qdrant collection.
        """
        self.vector_store = vector_store
        self.document_processor = document_processor
        self.collection_name = collection_name

    async def process_data(self):
        """
        Checks if data exists and processes the document if necessary.
        """
        has_data = self._check_collection_has_data()
        if not has_data:
            docs = self._load_and_split_document()
            self.vector_store.add_documents(docs)
        else:
            print(f"Collection has data. No processing needed.")

    def _check_collection_has_data(self) -> bool:
        """
        Checks if the Qdrant collection has data.
        Assumes collection exists.
        """
        try:
            collection_info = self.vector_store.client.get_collection(collection_name=self.collection_name)
            has_data = collection_info.points_count != None and collection_info.points_count > 0
            print(f"Collection {self.collection_name} has data: {has_data}")
            return has_data
        except Exception as e:
             print(f"Error getting collection info for {self.collection_name}: {e}")
             raise e

    def _load_and_split_document(self):
        """
        Loads and splits the document using the DocumentProcessor.
        """
        return self.document_processor.process_document()