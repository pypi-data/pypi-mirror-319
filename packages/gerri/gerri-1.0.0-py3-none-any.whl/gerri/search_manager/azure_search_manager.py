"""
search_index_manager.py

This module provides a SearchIndexManager class to manage Azure Search service operations.

Features:
1. Create and manage a search index in Azure Cognitive Search.
2. Index documents from Azure Blob Storage into the search index.
3. Index all documents (regardless of modification status) from Azure Blob Storage.
4. Index new or modified documents from Azure Blob Storage once.
5. Create an Azure-managed indexer that automatically indexes new or modified files on a schedule.
6. Search indexed documents using full-text search.

Supported File Types:
1. **Markdown Files (`.md`)**: Treated as plain text and indexed in their entirety.
2. **Plain Text Files (`.txt`)**: Fully supported and indexed.
3. **Code Files (`.py`, `.cpp`, `.java`, etc.)**: Treated as plain text and indexed in their entirety.
4. **Documents Supported by Azure Form Recognizer**(list):

   - **PDFs (`.pdf`)**: Text and structure extracted and indexed.
   - **Images (`.jpeg`, `.png`, etc.)**: Text from OCR and additional data extracted and indexed.

5. **Unsupported/Binary Files**(list):

   - Files not supported by the current implementation (e.g., `.exe`, `.zip`) may produce empty results and should be filtered at the blob level.

Limitations:
- Binary files or unsupported extensions (e.g., `.exe`, `.zip`) are not explicitly handled and may result in empty or unusable index entries.
- The indexing scheme treats all text-based files uniformly as plain text, without syntax-specific processing for code files.

The Azure Search resource information is read from environment variables or provided via a configuration dictionary.
"""

import os
import time
import base64
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchableField,
    SearchIndexer,
    SearchIndexerDataSourceConnection,
    IndexingSchedule
)
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
from gerri.blob_manager.blob_storage_manager import BlobStorageManager

# Load environment variables
load_dotenv()

def encode_key(blob_name):
    """
    Encodes the document key to a URL-safe Base64 string.

    Args:
        blob_name (str): The original blob name.

    Returns:
        str: A sanitized document key.
    """
    return base64.urlsafe_b64encode(blob_name.encode("utf-8")).decode("utf-8").rstrip("=")

class SearchIndexManager:
    """
    A class to manage Azure Search service operations, with support for extracting and enriching file content.
    """

    def __init__(self, config=None):
        """
        Initializes the SearchIndexManager with Azure Search and Form Recognizer credentials.

        Args:
            config (dict): Configuration options to override environment variables.
        """
        if config is None:
            config = {}

        self.endpoint = config.get("endpoint", os.getenv("AZURE_SEARCH_ENDPOINT"))
        self.key = config.get("key", os.getenv("AZURE_SEARCH_KEY"))
        self.form_recognizer_endpoint = config.get("form_recognizer_endpoint", os.getenv("FORM_RECOGNIZER_ENDPOINT"))
        self.form_recognizer_key = config.get("form_recognizer_key", os.getenv("FORM_RECOGNIZER_KEY"))

        if not self.endpoint or not self.key:
            raise ValueError("Azure Search endpoint and key must be provided")

        if not self.form_recognizer_endpoint or not self.form_recognizer_key:
            raise ValueError("Form Recognizer endpoint and key must be provided")

        self.search_index_client = SearchIndexClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))
        self.indexer_client = SearchIndexerClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))
        self.form_recognizer_client = DocumentAnalysisClient(endpoint=self.form_recognizer_endpoint, credential=AzureKeyCredential(self.form_recognizer_key))

    def create_index(self, index_name):
        """
        Creates a search index with default fields, including a key field.

        Args:
            index_name (str): Name of the index to create.

        Returns:
            None
        """
        fields = [
            SearchableField(name="id", type="Edm.String", key=True, filterable=True),
            SearchableField(name="file_name", type="Edm.String", filterable=True),
            SearchableField(name="relative_file_location", type="Edm.String", filterable=True),
            SearchableField(name="file_content", type="Edm.String", filterable=False, searchable=True),
            SearchableField(name="file_text", type="Edm.String", filterable=False, searchable=True),
            SearchableField(name="file_image_summary", type="Edm.String", filterable=False, searchable=False),
            SearchableField(name="file_last_modified", type="Edm.DateTimeOffset", filterable=True, sortable=True),  # Added for tracking updates
        ]

        index = SearchIndex(name=index_name, fields=fields)
        self.search_index_client.create_index(index)
        print(f"Index {index_name} created with default fields.")

    def extract_file_data(self, blob_client):
        """
        Extracts data from a file using supported formats.

        Args:
            blob_client: A BlobClient instance for the target file.

        Returns:
            dict: A dictionary containing extracted file data.
        """
        blob_name = blob_client.blob_name
        blob_content = blob_client.download_blob().readall()

        sanitized_id = encode_key(blob_name)

        if blob_name.lower().endswith(".md"):
            file_text = blob_content.decode('utf-8', errors='ignore')
            return {
                "id": sanitized_id,
                "file_name": blob_name,
                "relative_file_location": f"{blob_client.container_name}/{blob_name}",
                "file_content": file_text,
                "file_text": file_text,
                "file_image_summary": "",
            }
        else:
            try:
                poller = self.form_recognizer_client.begin_analyze_document("prebuilt-document", blob_content)
                result = poller.result()

                text_content = " ".join([page.content for page in result.pages])
                image_summary = " ".join(
                    [line.content for page in result.pages for line in page.lines if line.appearance and line.appearance.style_name == "handwriting"]
                )

                return {
                    "id": sanitized_id,
                    "file_name": blob_name,
                    "relative_file_location": f"{blob_client.container_name}/{blob_name}",
                    "file_content": blob_content.decode('utf-8', errors='ignore'),
                    "file_text": text_content,
                    "file_image_summary": image_summary,
                }
            except Exception as e:
                print(f"Error processing file {blob_name}: {e}")
                return {
                    "id": sanitized_id,
                    "file_name": blob_name,
                    "relative_file_location": f"{blob_client.container_name}/{blob_name}",
                    "file_content": "",
                    "file_text": "",
                    "file_image_summary": "",
                }

    def index_from_blob(self, blob_storage_manager, container_name, index_name, folder_path=None):
        """
        Indexes all documents from a container or folder in Azure Blob Storage.

        Args:
            blob_storage_manager (BlobStorageManager): Instance of BlobStorageManager to interact with blob storage.
            container_name (str): Name of the blob container.
            index_name (str): Name of the search index.
            folder_path (str, optional): Path to the folder in the blob container. If None, indexes the entire container.

        Returns:
            None
        """
        blob_storage_manager.container_client = blob_storage_manager.blob_service_client.get_container_client(container_name)
        blob_list = blob_storage_manager.container_client.list_blobs(name_starts_with=folder_path or "")

        search_client = SearchClient(endpoint=self.endpoint, index_name=index_name, credential=AzureKeyCredential(self.key))

        documents = []
        for blob in blob_list:
            blob_client = blob_storage_manager.container_client.get_blob_client(blob)
            file_data = self.extract_file_data(blob_client)
            documents.append(file_data)

        if documents:
            search_client.upload_documents(documents=documents)
            print(f"Indexed {len(documents)} documents into {index_name} from container {container_name}.")
        else:
            print(f"No documents found in container {container_name} (folder: {folder_path or 'entire container'}).")

    def search_index(self, index_name, search_query, topNDocs=5):
        """
        Searches the specified index using the given query and returns results in JSON format.

        Args:
            index_name (str): Name of the search index.
            search_query (str): The query string to search for.
            topNDocs (int): Number of top results to fetch.

        Returns:
            dict: Search results including file name, file content, and search score.
        """
        search_client = SearchClient(endpoint=self.endpoint, index_name=index_name, credential=AzureKeyCredential(self.key))

        results = search_client.search(
            search_query,
            include_total_count=True,
            query_type="simple",
            select=["file_name", "file_content"],
            top=topNDocs
        )

        results_json = {
            "total_count": results.get_count(),
            "value": [
                {
                    "file_name": result.get("file_name", None),
                    "file_content": result.get("file_content", None),
                    "search_score": result["@search.score"]
                }
                for result in results
            ]
        }
        return results_json
    
    def create_indexer(self, data_source_name, indexer_name, index_name, container_name, folder_path=None, interval="PT24H"):
        """
        Creates an Azure-managed indexer for periodic indexing.

        Args:
            data_source_name (str): Name of the data source connection.
            indexer_name (str): Name of the indexer to create.
            index_name (str): Name of the search index.
            container_name (str): Name of the Azure Blob Storage container.
            folder_path (str, optional): Folder path in the blob container. If None, it indexes the entire container.
            interval (str): Indexing interval in ISO 8601 duration format (e.g., "PT24H" for 24 hours).

        Returns:
            None
        """
        data_source_connection = SearchIndexerDataSourceConnection(
            name=data_source_name,
            type="azureblob",
            connection_string=os.getenv("BLOB_CONNECTION_STRING"),
            container={"name": container_name, "query": folder_path},
        )

        self.indexer_client.create_data_source_connection(data_source_connection)

        indexer = SearchIndexer(
            name=indexer_name,
            data_source_name=data_source_name,
            target_index_name=index_name,
            schedule=IndexingSchedule(interval=interval),
        )

        self.indexer_client.create_indexer(indexer)
        print(f"Indexer {indexer_name} created to run every {interval}.")

if __name__ == "__main__":
    # Load configuration from environment variables
    config = {
        "endpoint": os.getenv("AZURE_SEARCH_ENDPOINT"),
        "key": os.getenv("AZURE_SEARCH_KEY"),
        "form_recognizer_endpoint": os.getenv("FORM_RECOGNIZER_ENDPOINT"),
        "form_recognizer_key": os.getenv("FORM_RECOGNIZER_KEY"),
    }

    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    blob_config = {
        "connection_string": os.getenv("BLOB_CONNECTION_STRING"),
        "container_name": os.getenv("BLOB_CONTAINER_NAME"),
    }

    indexer_name = os.getenv("AZURE_SEARCH_INDEXER_NAME", "periodicindexer")
    indexer_interval_seconds = int(os.getenv("AZURE_SEARCH_INDEXER_INTERVAL_IN_SECONDS", 86400))  # Default 24 hours
    indexer_interval_iso = f"PT{indexer_interval_seconds // 3600}H"  # Convert to ISO 8601 format

    blob_manager = BlobStorageManager(config=blob_config)
    manager = SearchIndexManager(config=config)

    # Uncomment to create the index
    # manager.create_index(index_name)

    # # Uncomment to index all documents from the blob container
    # manager.index_from_blob(blob_manager, blob_config["container_name"], index_name=index_name, folder_path=None)

    # # Uncomment to create an Azure-managed indexer
    # manager.create_indexer(
    #     data_source_name="my-blob-datasource",
    #     indexer_name=indexer_name,
    #     index_name=index_name,
    #     container_name=blob_config["container_name"],
    #     folder_path=None,
    #     interval=indexer_interval_iso
    # )

    # Perform a search query
    search_query = input("Enter a search query: ")
    search_results = manager.search_index(index_name, search_query)
    print("Search Results:", search_results)

