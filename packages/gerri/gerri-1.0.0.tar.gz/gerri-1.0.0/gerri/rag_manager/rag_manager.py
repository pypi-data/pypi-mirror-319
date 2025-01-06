"""
rag_manager.py

This module provides the RAGManager class, which facilitates Retrieval-Augmented Generation (RAG)-based interactions by integrating Azure Cognitive Search, a Language Learning Model (LLM), and Cosmos DB. 

The core functionality of this module includes:
1. Retrieving relevant documents from an Azure Cognitive Search index.
2. Generating responses from an LLM (e.g., OpenAI or Ollama) using the retrieved documents as context.
3. Streaming LLM responses when required.
4. Storing interaction data (queries and responses) in Cosmos DB.

Use Cases:
- Build a conversational AI system capable of leveraging domain-specific knowledge stored in a search index.
- Enhance LLM responses by grounding them in relevant retrieved data.
- Maintain an auditable interaction history using Cosmos DB.

Example Features:
- **Contextual Search**: Uses Azure Cognitive Search to find relevant documents based on a query.
- **LLM Integration**: Leverages LLMs to provide human-like responses grounded in retrieved knowledge.
- **Data Persistence**: Stores chat interactions (queries, responses, and metadata) in Cosmos DB.
- **Streamed Responses**: Supports real-time response streaming for conversational systems.

Supported Integrations:
- **Search Index**: Azure Cognitive Search.
- **LLMs**: OpenAI, Ollama, or Azure OpenAI models.
- **Database**: Cosmos DB for storing interaction data.

""" 
import os
import logging
from datetime import datetime
from gerri.search_manager.azure_search_manager import SearchIndexManager
from gerri.llm_manager.openai_manager.azure_openai_manager import AzureOpenAIManager
from gerri.llm_manager.ollama_manager.ollama_manager import OllamaChat
from gerri.database_manager.cosmo_db_manager import ChatbotDatabaseManager

# Configure logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger("azure.cosmos").setLevel(logging.WARNING)
logging.getLogger("azure.core").setLevel(logging.WARNING)
logging.getLogger("azure.identity").setLevel(logging.WARNING)

class RAGManager:
    """
    Retrieval-Augmented Generation (RAG) Manager

    This class implements the RAG pipeline to handle user queries by:
    1. Searching an Azure Cognitive Search index for relevant documents.
    2. Using a selected LLM (AzureOpenAIManager or OllamaChat) to generate responses with retrieved context.
    3. Storing chat interactions in Azure Cosmos DB.

    Features:
    - Supports both AzureOpenAIManager and OllamaChat for LLM responses.
    - Enables both standard and streamed chat interactions.
    - Stores user interactions and responses in Cosmos DB.

    """

    def __init__(self, search_manager, llm_manager, cosmos_config, system_prompt):
        """
        Initializes the RAGManager.

        Args:
            search_manager (SearchIndexManager): An instance of the search manager.
            llm_manager (Union[AzureOpenAIManager, OllamaChat]): An instance of the LLM manager.
            cosmos_config (dict): Configuration dictionary for Cosmos DB.
            system_prompt (str): The system prompt to guide the LLM.
        """
        self.search_manager = search_manager
        self.llm_manager = llm_manager
        self.cosmos_manager = ChatbotDatabaseManager(config=cosmos_config)
        self.system_prompt = system_prompt

    def search_index(self, query, topNDocs=5):
        """
        Searches the Azure Cognitive Search index.

        Args:
            query (str): The search query.
            topNDocs (int): Number of documents to retrieve.

        Returns:
            dict: A dictionary of documents retrieved from the search index.
        """
        index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
        return self.search_manager.search_index(index_name, query, topNDocs=topNDocs)

    def chat(self, user_id, chat_id, query, temperature=0.3):
        """
        Executes a RAG-based chat interaction.

        Args:
            user_id (str): The ID of the user.
            chat_id (str): The ID of the chat.
            query (str): The user's query.
            temperature (float): The temperature for the LLM response.

        Returns:
            dict: The final response.
        """
        # Step 1: Retrieve context from search index
        context_documents = self.search_index(query)
        documents = context_documents.get('value', [])
        context = "\n".join([doc["file_content"] for doc in documents])

        # Step 2: Generate a response using the LLM
        if isinstance(self.llm_manager, AzureOpenAIManager):
            llm_response = self.llm_manager.chat(
                user_input=query,
                prompt=f"{self.system_prompt}\nContext from search is: {context}"
            )
        elif isinstance(self.llm_manager, OllamaChat):
            llm_response = "".join(
                chunk for chunk in self.llm_manager.chat(
                    user_input=query,
                    prompt=f"{self.system_prompt}\nContext from search is: {context}"
                )
            )

        # Step 3: Store the interaction in Cosmos DB
        item = {
            "id": chat_id,
            "user_id": user_id,
            "request": [
                {"content": query, "time": datetime.utcnow().isoformat(), "sentiment": "neutral"}
            ],
            "response": [
                {"content": llm_response, "time": datetime.utcnow().isoformat(), "sentiment": "neutral"}
            ],
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "time": datetime.utcnow().strftime("%H:%M:%S")
        }
        self.cosmos_manager.create_or_update_chat(item)

        return {
            "query": query,
            "context": context_documents,
            "response": llm_response
        }

    def chat_streamed(self, user_id, chat_id, query, temperature=0.3):
        """
        Executes a RAG-based chat interaction with streaming support.

        Args:
            user_id (str): The ID of the user.
            chat_id (str): The ID of the chat.
            query (str): The user's query.
            temperature (float): The temperature for the LLM response.

        Yields:
            str: The response stream.
        """
        # Step 1: Retrieve context from search index
        context_documents = self.search_index(query)
        documents = context_documents.get('value', [])
        context = "\n".join([doc["file_content"] for doc in documents])

        # Step 2: Stream a response using the LLM
        if isinstance(self.llm_manager, AzureOpenAIManager):
            response_stream = self.llm_manager.chat_streamed(
                user_input=query,
                prompt=f"{self.system_prompt}\nContext from search is: {context}"
            )
        elif isinstance(self.llm_manager, OllamaChat):
            response_stream = self.llm_manager.chat(
                user_input=query,
                prompt=f"{self.system_prompt}\nContext from search is: {context}"
            )

        # Store the interaction in Cosmos DB
        full_response = ""
        for chunk in response_stream:
            full_response += chunk
            yield chunk

        item = {
            "id": chat_id,
            "user_id": user_id,
            "request": [
                {"content": query, "time": datetime.utcnow().isoformat(), "sentiment": "neutral"}
            ],
            "response": [
                {"content": full_response, "time": datetime.utcnow().isoformat(), "sentiment": "neutral"}
            ],
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "time": datetime.utcnow().strftime("%H:%M:%S")
        }
        self.cosmos_manager.create_or_update_chat(item)

# Example usage
if __name__ == "__main__":
    cosmos_config = {
        "COSMOS_DB_ENDPOINT": os.getenv("COSMOS_DB_ENDPOINT"),
        "COSMOS_DB_KEY": os.getenv("COSMOS_DB_KEY"),
        "COSMOS_DB_DATABASE_NAME": os.getenv("COSMOS_DB_DATABASE_NAME"),
        "COSMOS_DB_CONTAINER_NAME": os.getenv("COSMOS_DB_CONTAINER_NAME")
    }

    # Choose LLM manager dynamically
    llm_type = os.getenv("LLM_TYPE", "azure_openai").lower()
    logging.info(f"Using LLM type: {llm_type}")
    if llm_type == "ollama":
        llm_manager = OllamaChat(model=os.getenv("OLLAMA_MODEL", "llama3.2"), temperature=os.getenv("TEMPERATURE", 1.0))
    else:
        llm_manager = AzureOpenAIManager(config={
            "OPENAI_ENDPOINT": os.getenv("OPENAI_ENDPOINT"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
            "OPENAI_DEPLOYMENT_ID": os.getenv("OPENAI_DEPLOYMENT_ID"),
            "OPENAI_API_VERSION": os.getenv("OPENAI_API_VERSION"),
            "TEMPERATURE": os.getenv("TEMPERATURE")
        })

    search_manager = SearchIndexManager(config={
        "endpoint": os.getenv("AZURE_SEARCH_ENDPOINT"),
        "key": os.getenv("AZURE_SEARCH_KEY")
    })

    system_prompt = os.getenv("SYSTEM_PROMPT", "You are an AI assistant that uses retrieved documents to provide accurate and helpful responses. Be concise and answer clearly.")

    rag_manager = RAGManager(
        search_manager=search_manager,
        llm_manager=llm_manager,
        cosmos_config=cosmos_config,
        system_prompt=system_prompt
    )

    user_id = input("Enter user ID: ")
    chat_id = input("Enter chat ID: ")
    user_query = input("Enter your query: ")
    temperature_default = float(os.getenv("TEMPERATURE", 0.3))
    response = rag_manager.chat(user_id, chat_id, user_query, temperature=temperature_default)
    print("Response:", response)
    # Example usage of streamed chat
    user_query_2 = input("Enter your query for streamed response: ")
    for chunk in rag_manager.chat_streamed(user_id, chat_id, user_query_2, temperature=temperature_default):
        print(chunk)
