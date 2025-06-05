from langchain_community.document_loaders import PyPDFLoader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, data_path: str):
        """
        Initializes the DocumentProcessor with the path to the PDF document.

        Args:
            data_path: The path to the PDF document.
        """
        self.data_path = data_path
        self.chunk_size = 1000
        self.chunk_overlap = 100

    def process_document(self):
        """
        Loads and splits the PDF document into chunks.

        Returns:
            A list of document chunks.
        """
        # Load the PDF
        loader = PyPDFLoader(self.data_path)
        documents = loader.load()

        # Split the documents
        print("Splitting the docs")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        docs = text_splitter.split_documents(documents)

        return docs

# You'll also need to ensure 'langchain' and 'pypdf' are in your requirements.txt
# and installed in your virtual environment for this to work. 