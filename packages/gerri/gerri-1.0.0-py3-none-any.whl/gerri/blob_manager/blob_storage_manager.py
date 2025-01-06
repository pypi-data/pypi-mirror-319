'''Blob Storage Manager for Gerri'''
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BlobStorageManager:
    '''Class to manage Azure Blob Storage operations'''
    def __init__(self, config=None):
        """
        Initializes the BlobStorageManager with Azure Blob Storage credentials.

        Args:
            config (dict): Configuration options to override environment variables.
                           Expected structure:
                           {
                               "connection_string": "your_connection_string",
                               "container_name": "your_container_name"
                           }
        """
        if config is None:
            config = {}

        self.connection_string = config.get("connection_string", os.getenv("BLOB_CONNECTION_STRING"))
        self.container_name = config.get("container_name", os.getenv("BLOB_CONTAINER_NAME"))
        
        if not self.connection_string or not self.container_name:
            raise ValueError("Azure Blob Storage connection string and container name must be provided")

        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def upload_file(self, file_path, blob_name):
        """
        Uploads a file to the blob storage. If the file exists, it will be replaced.

        Args:
            file_path (str): Path to the file to upload.
            blob_name (str): Name of the blob in the container.

        Returns:
            None

        Example:
            manager.upload_file("path/to/local/file.txt", "file.txt")
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"File {file_path} uploaded to blob {blob_name}.")

    def upload_folder(self, folder_path, destination_folder=None):
        """
        Uploads all files in a given folder to the blob storage.

        Args:
            folder_path (str): Path to the folder containing files to upload.
            destination_folder (str): Name of the destination folder in the blob storage. If not provided, 
                                      the original folder name will be used.

        Returns:
            None

        Example:
            manager.upload_folder("path/to/local/folder", "destination_folder")
        """
        if destination_folder is None:
            destination_folder = os.path.basename(folder_path)
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path).replace("\\", "/")
                blob_name = f"{destination_folder}/{relative_path}"
                self.upload_file(file_path, blob_name)

    def download_file(self, blob_name, download_path):
        """
        Downloads a file from the blob storage.

        Args:
            blob_name (str): Name of the blob in the container.
            download_path (str): Path to save the downloaded file.

        Returns:
            None

        Example:
            manager.download_file("file.txt", "path/to/download/file.txt")
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        with open(download_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f"Blob {blob_name} downloaded to {download_path}.")

    def delete_file(self, blob_name):
        """
        Deletes a file from the blob storage.

        Args:
            blob_name (str): Name of the blob in the container.

        Returns:
            None

        Example:
            manager.delete_file("file.txt")
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
        print(f"Blob {blob_name} deleted.")

    def get_file_metadata(self, blob_name):
        """
        Retrieves metadata and properties of a file in the blob storage.

        Args:
            blob_name (str): Name of the blob in the container.

        Returns:
            dict: Metadata and properties of the blob. The dictionary includes:
                - **metadata** (dict): Custom metadata associated with the blob.
                - **last_modified** (datetime): The last modification time of the blob.
                - **size** (int): The size of the blob in bytes.
                - **content_type** (str): The MIME type of the blob.

        Example:
            metadata = manager.get_file_metadata("file.txt")
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        properties = blob_client.get_blob_properties()
        metadata = properties.metadata
        last_modified = properties.last_modified
        return {
            "metadata": metadata,
            "last_modified": last_modified,
            "size": properties.size,
            "content_type": properties.content_settings.content_type
        }

    def file_exists(self, blob_name):
        """
        Checks if a file exists in the blob storage.

        Args:
            blob_name (str): Name of the blob in the container.

        Returns:
            bool: True if the blob exists, False otherwise.

        Example:
            exists = manager.file_exists("file.txt")
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.exists()

# Example usage
if __name__ == "__main__":
    config = {
        "connection_string": os.getenv("BLOB_CONNECTION_STRING"),
        "container_name": os.getenv("BLOB_CONTAINER_NAME")
    }
    manager = BlobStorageManager(config=config)
    manager.upload_file("requirements.txt", "requirements.txt")
    manager.upload_folder("output", "recipes_md_files")
    manager.download_file("requirements.txt", "requirements_downloaded.txt")
    print(manager.get_file_metadata("requirements.txt"))
    print(manager.file_exists("requirements.txt"))
    manager.delete_file("requirements.txt")