# Gerri Library

The **Gerri Library** (Giant Eagle Retrieval and Response Interface) is a comprehensive Python package designed for managing and orchestrating various functionalities such as database interactions, API management, large language model integration, and more.

## Features

- **Blob Manager**: Manage Azure Blob Storage for file and folder operations.
- **API Manager**: Handle API-related functionalities (future development).
- **Content Filters**: Implement and manage content filtering strategies.
- **Database Manager**: Interact with Cosmos DB and manage database operations.
- **LLM Manager**: Integrate with OpenAI, Hugging Face, and other LLM APIs.
- **Search Manager**: Utilize Azure Search for content search capabilities.
- **RAG Manager**: Manage Retrieval-Augmented Generation workflows.
- **Summary Tag Manager**: Provide summary tagging functionality.
- **Utilities**: General utility functions for common tasks.

## Installation

To install the Gerri Library, use the following command:

```bash
pip install gerri
```

For development purposes, install the package in editable mode:

```bash
pip install -e .
```

## Requirements

Ensure the dependencies listed in `gerri/requirements.txt` are installed:

```bash
pip install -r gerri/requirements.txt
```

## Usage

Here are some examples of how to use the library:

### Blob Manager


    from gerri.blob_manager import blob_storage_manager

    manager = blob_storage_manager.BlobStorageManager(config={
        "connection_string": "your_connection_string",
        "container_name": "your_container_name"
    })
    manager.upload_file("example.txt", "blob_name")


### LLM Manager (OpenAI Example)


    from gerri.llm_manager.openai_manager import openai_manager

    openai_instance = openai_manager.OpenAIManager(api_key="your_openai_api_key")
    response = openai_instance.generate_text(prompt="Hello, world!")
    print(response)


## Documentation

Full documentation is available in the `docs/` directory or online (if hosted on platforms like Read the Docs).

## Project Structure

- **`blob_manager/`**: Azure Blob Storage management.
- **`api_manager/`**: API management utilities (future development).
- **`content_filters/`**: Content filtering tools.
- **`database_manager/`**: Database management with Cosmos DB.
- **`llm_manager/`**: Large language model integrations, including (list):

  - OpenAI
  - Hugging Face
  - Ollama Manager
  
- **`rag_manager/`**: Retrieval-Augmented Generation workflows.
- **`search_manager/`**: Azure Search integration.
- **`summary_tag_manager/`**: Summary tagging.
- **`utilities/`**: General utility functions.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.

## Environment Variables Configuration

This file provides a description of the environment variables required for the Recipe Generator project. These variables are stored in the `.env` file and are used to configure various services and APIs.

## Environment Variables

### OpenAI Configuration
- **OPENAI_ENDPOINT**: The endpoint for the OpenAI service.
- **OPENAI_API_KEY**: The API key for accessing the OpenAI service.
- **OPENAI_DEPLOYMENT_ID**: The deployment ID for the OpenAI model.
- **OPENAI_API_VERSION**: The version of the OpenAI API to use.
- **TEMPERATURE**: The temperature setting for the OpenAI model.

### Image API Configuration
- **IMAGE_API_ENDPOINT**: The endpoint for the image generation API.
- **IMAGE_API_KEY**: The API key for accessing the image generation API.
- **IMAGE_DEPLOYMENT_ID**: The deployment ID for the image generation model.

### Content Safety Configuration
- **CONTENT_SAFETY_ENDPOINT**: The endpoint for the content safety API.
- **CONTENT_SAFETY_KEY**: The API key for accessing the content safety API.

### Cosmos DB Configuration
- **COSMOS_DB_ENDPOINT**: The endpoint for the Cosmos DB service.
- **COSMOS_DB_KEY**: The key for accessing the Cosmos DB service.
- **COSMOS_DB_DATABASE_NAME**: The name of the Cosmos DB database.
- **COSMOS_DB_CONTAINER_NAME**: The name of the Cosmos DB container.
- **COSMOS_DB_PARTITION_KEY**: The partition key for the Cosmos DB container.

### Recipe Generation Prompt
- **RECIPE_GENERATION_PROMPT**: The prompt used for generating recipes. This should be a JSON string with specific guidelines for the recipe generation.

### Azure Blob Storage Configuration
- **BLOB_CONNECTION_STRING**: The connection string for accessing Azure Blob Storage.
- **BLOB_CONTAINER_NAME**: The name of the blob container where recipe files are stored.
- **BLOB_RECIPE_FOLDER**: The folder within the blob container where recipe files are stored.

### Azure Search Configuration
- **AZURE_SEARCH_ENDPOINT**: The endpoint for the Azure Search service.
- **AZURE_SEARCH_KEY**: The API key for accessing the Azure Search service.
- **AZURE_SEARCH_INDEX_NAME**: The name of the Azure Search index.
- **AZURE_SEARCH_INDEXER_NAME**: The name of the Azure Search indexer.
- **AZURE_SEARCH_INDEXER_INTERVAL_IN_SECONDS**: The interval in seconds for the Azure Search indexer to run.

### Form Recognizer Configuration
- **FORM_RECOGNIZER_ENDPOINT**: The endpoint for the Azure Form Recognizer service.
- **FORM_RECOGNIZER_KEY**: The API key for accessing the Azure Form Recognizer service.

### System Prompt
- **SYSTEM_PROMPT**: The system prompt used for generating recipes. This should be a JSON string with specific guidelines for the recipe generation.

### LLM Type
- **LLM_TYPE**: The type of language model to use (e.g., `openai` or `ollama`). ollama will use local LLM and will require OLLAMA to be installed on the machine running the code. 
- **OLLAMA_MODEL**: specify the Ollama model to be used like LLAMA3.1 or LLAMA3.2