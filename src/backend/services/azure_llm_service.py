import os
from langchain_core.embeddings import Embeddings # Import Embeddings base type
from langchain_core.language_models.chat_models import BaseChatModel # Import BaseChatModel base type
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_openai.chat_models import AzureChatOpenAI

class AzureLLMService:
    def __init__(self, vector_size):
        """
        Initializes the AzureLLMService by loading Azure configuration from environment variables.
        """
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
        self.azure_openai_chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT") # Assuming a separate env var for chat deployment
        self.vector_size = vector_size

    def get_embeddings(self) -> Embeddings:
        """
        Provides an instance of AzureOpenAIEmbeddings.

        Returns:
            An instance of AzureOpenAIEmbeddings.
        """

        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=self.azure_openai_endpoint,
            azure_deployment=self.azure_openai_embedding_deployment,
            chunk_size=self.vector_size
        )
        return embeddings

    def get_llm(self) -> BaseChatModel:
        """
        Provides an instance of AzureChatOpenAI.

        Returns:
            An instance of AzureChatOpenAI.
        """
        if not all([self.azure_openai_endpoint, self.azure_openai_api_key, self.azure_openai_chat_deployment]):
             raise ValueError("Azure OpenAI chat configuration is incomplete.")

        llm = AzureChatOpenAI(
            azure_endpoint=self.azure_openai_endpoint,
            deployment_name=self.azure_openai_chat_deployment
        )
        return llm

    def get_embedding_vector_size(self, embeddings: Embeddings) -> int:
        """
        Determines the vector size from an embeddings instance.

        Args:
            embeddings: An initialized embeddings instance.

        Returns:
            The size of the embedding vectors.
        """
        try:
            # Embed a dummy query to get the vector size.
            vector_size = len(embeddings.embed_query("This is a test query"))
            print(f"Determined embedding vector size: {vector_size}")
            return vector_size
        except Exception as e:
            raise RuntimeError(f"Could not determine vector size from embeddings. Check Azure config and embedding deployment. Error: {e}") from e