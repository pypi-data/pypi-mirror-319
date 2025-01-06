'''Cosmos DB Manager to store chat request response pairs'''
import os
import json
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotDatabaseManager:
    def __init__(self, config=None):
        """
        Initializes the ChatbotDatabaseManager with Cosmos DB credentials.

        Args:
            config (dict): Configuration options to override environment variables.
                           Expected structure:
                           ```python
                           {
                               "COSMOS_DB_ENDPOINT": "your_cosmos_db_endpoint",
                               "COSMOS_DB_KEY": "your_cosmos_db_key",
                               "COSMOS_DB_DATABASE_NAME": "your_database_name",
                               "COSMOS_DB_CONTAINER_NAME": "your_container_name"
                           }
                           ```python
        """
        if config is None:
            config = {}

        self.endpoint = config.get("COSMOS_DB_ENDPOINT", os.getenv("COSMOS_DB_ENDPOINT"))
        self.key = config.get("COSMOS_DB_KEY", os.getenv("COSMOS_DB_KEY"))
        self.database_name = config.get("COSMOS_DB_DATABASE_NAME", os.getenv("COSMOS_DB_DATABASE_NAME"))
        self.container_name = config.get("COSMOS_DB_CONTAINER_NAME", os.getenv("COSMOS_DB_CONTAINER_NAME"))

        if not all([self.endpoint, self.key, self.database_name, self.container_name]):
            raise ValueError("Cosmos DB credentials and names must be provided")

        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )

    def create_item(self, item):
        """
        Creates an item in the container.

        Args:

            item (dict): The item to create. Must contain the following keys:
            
                - **id** (str): The unique identifier for the item.
                - **user_id** (str): The ID of the user associated with the item.
                - **request** (list): A list of request dictionaries. Each dictionary contains:
                
                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.
                    
                - **response** (list): A list of response dictionaries. Each dictionary contains:
                
                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.
                    
                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:

            item = {
                "id": "1",
                "user_id": "user123",
                "request": [{"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
                ],
                "response": [{"content": "I'm good, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
                ],
                "date": "2023-11-01",
                "time": "12:01:00"
            }
            manager.create_item(item)

        Returns:

            None
        """
        try:
            self.container.create_item(body=item)
            print("Item created successfully")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred: {e.message}")

    def read_item(self, item_id):
        """
        Reads an item from the container by its ID.

        Args:
            item_id (str): The ID of the item to read.

        Returns:
            dict: The item retrieved from the container, structured as follows:

            - **id** (str): The unique identifier of the item.
            - **user_id** (str): The user associated with the item.
            - **request** (list): A list of request dictionaries containing:
                - **content** (str): The content of the request.
                - **time** (str): The timestamp of the request.
                - **sentiment** (str): The sentiment of the request.
            - **response** (list): A list of response dictionaries containing:
                - **content** (str): The content of the response.
                - **time** (str): The timestamp of the response.
                - **sentiment** (str): The sentiment of the response.
            - **date** (str): The date of the interaction.
            - **time** (str): The time of the interaction.

        Example:
            ```python
            item = manager.read_item("1")
            print(item)
            ```
        """
        try:
            item = self.container.read_item(item=item_id, partition_key=item_id)
            return item
        except exceptions.CosmosResourceNotFoundError:
            print(f"Item with ID {item_id} not found")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred: {e.message}")
    
    def read_item_by_user_id(self, user_id):
        """
        Reads items from the container by user_id.

        Args:
            user_id (str): The user_id of the items to read.

        Returns:
            list: A list of items associated with the given user_id. Each item is structured as follows:

            - **id** (str): The unique identifier of the item.
            - **user_id** (str): The user associated with the item.
            - **request** (list): A list of request dictionaries containing:
                - **content** (str): The content of the request.
                - **time** (str): The timestamp of the request.
                - **sentiment** (str): The sentiment of the request.
            - **response** (list): A list of response dictionaries containing:
                - **content** (str): The content of the response.
                - **time** (str): The timestamp of the response.
                - **sentiment** (str): The sentiment of the response.
            - **date** (str): The date of the interaction.
            - **time** (str): The time of the interaction.

        Example:
            ```python
            items = manager.read_item_by_user_id("user123")
            print(items)
            ```
        """

        query = "SELECT * FROM c WHERE c.user_id = @user_id"
        items = list(self.container.query_items(query=query, parameters=[{"name": "@user_id", "value": user_id}], enable_cross_partition_query=True))
        return items
    
    def read_item_by_date_range(self, date_begin, date_end):
        """
        Reads items from the container within a specified date range.

        Args:
            date_begin (str): The start date and time of the range in ISO 8601 format.
                Example: "2023-11-01T00:00:00Z"
            date_end (str): The end date and time of the range in ISO 8601 format.
                Example: "2023-11-30T23:59:59Z"

        Returns:
            list: A list of items within the specified date range. Each item is structured as follows:

            - **id** (str): The unique identifier of the item.
            - **user_id** (str): The user associated with the item.
            - **request** (list): A list of request dictionaries containing:
                - **content** (str): The content of the request.
                - **time** (str): The timestamp of the request.
                - **sentiment** (str): The sentiment of the request.
            - **response** (list): A list of response dictionaries containing:
                - **content** (str): The content of the response.
                - **time** (str): The timestamp of the response.
                - **sentiment** (str): The sentiment of the response.
            - **date** (str): The date of the interaction.
            - **time** (str): The time of the interaction.

        Example:
            ```python
            items = manager.read_item_by_date_range("2023-11-01T00:00:00Z", "2023-11-30T23:59:59Z")
            print(items)
            ```
        """

        query = """
        SELECT * FROM c 
        WHERE CONCAT(c.date, 'T', c.time, 'Z') >= @date_begin 
        AND CONCAT(c.date, 'T', c.time, 'Z') <= @date_end
        """
        items = list(self.container.query_items(
            query=query,
            parameters=[
                {"name": "@date_begin", "value": date_begin},
                {"name": "@date_end", "value": date_end}
            ],
            enable_cross_partition_query=True
        ))
        logging.info(f"Retrieved {len(items)} items")
        for item in items:
            logging.info(f"Item: {item}")
        return items

    def update_item(self, item_id, updated_item):
        """
        Updates an existing item in the container.

        Args:

            item_id (str): The ID of the item to update.
            updated_item (dict): The updated item with the following required structure:
                - **id** (str): The unique identifier for the item.
                - **user_id** (str): The user associated with the item.
                - **request** (list): A list of request dictionaries containing:

                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.

                - **response** (list): A list of response dictionaries containing:

                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.

                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:
        
            updated_item = {
                "id": "1",
                "user_id": "user123",
                "request": [{"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
                ],
                "response": [{"content": "I'm great, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
                ],
                "date": "2023-11-01",
                "time": "12:01:00"
            }
            manager.update_item("1", updated_item)
            

        Returns:

            None

        """

        try:
            item = self.container.read_item(item=item_id, partition_key=item_id)
            for key, value in updated_item.items():
                item[key] = value
            self.container.replace_item(item=item_id, body=item)
            print("Item updated successfully")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Item with ID {item_id} not found")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred: {e.message}")

    def delete_item(self, item_id):
        """
        Deletes an item from the container by its ID.

        Args:
            item_id (str): The unique identifier of the item to be deleted.

        Example:
            ```python
            manager.delete_item("1")
            ```

        Returns:
            None
        """
        try:
            self.container.delete_item(item=item_id, partition_key=item_id)
            print("Item deleted successfully")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Item with ID {item_id} not found")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred: {e.message}")

    def upsert_item(self, item):
        """
        Upserts an item in the container.

        Args:

            item (dict): The item to upsert. Must contain the following keys:
            
                - **id** (str): The unique identifier for the item.
                - **user_id** (str): The ID of the user associated with the item.
                - **request** (list): A list of request dictionaries. Each dictionary must contain:

                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.

                - **response** (list): A list of response dictionaries. Each dictionary must contain:

                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.

                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:
            item = {
                "id": "1",
                "user_id": "user123",
                "request": [{"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
                ],
                "response": [{"content": "I'm good, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
                ],
                "date": "2023-11-01",
                "time": "12:01:00"
            }
            manager.upsert_item(item)

        Returns:

            None
            
        """
        try:
            self.container.upsert_item(body=item)
            print("Item upserted successfully")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred: {e.message}")

    def get_chat_request_response(self, item_id, chat_dict):
        """
        Upserts an item in the container.

        Args:

            item (dict): The item to upsert with the following required structure:
                - **id** (str): The unique identifier for the item.
                - **user_id** (str): The user associated with the item.
                - **request** (list): A list of request dictionaries containing:

                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.

                - **response** (list): A list of response dictionaries containing:

                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.

                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:
            
            item = {
                "id": "1",
                "user_id": "user123",
                "request": [{"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
                ],
                "response": [{"content": "I'm good, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
                ],
                "date": "2023-11-01",
                "time": "12:01:00"
            }
            manager.upsert_item(item)
            

        Returns:

            None

        """

        required_keys = ['external_id', 'chat_timestamp_request', 'chat_timestamp_response',
                         'request_text', 'response_text', 'transfer', 'id',
                         'references', 'ttl', 'titles']
        missing_keys = [key for key in required_keys if key not in chat_dict]
        if missing_keys:
            raise ValueError(f"Missing keys in chat_dict: {', '.join(missing_keys)}")
        chat_request_response = {
            'id': item_id,
            'id': '1',
            'chat_dict': chat_dict,
            'ttl': 60 * 60 * 24 * 30
        }
        return chat_request_response

    def get_latest_item(self):
        """
        Retrieves the latest item from the container based on the update or creation time.

        Returns:
            dict: The latest item in the container, structured as follows:
                - **id** (str): The unique identifier for the item.
                - **user_id** (str): The user associated with the item.
                - **request** (list): A list of request dictionaries containing:
                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.
                - **response** (list): A list of response dictionaries containing:
                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.
                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:
            ```python
            latest_item = manager.get_latest_item()
            print(latest_item)
            ```
        """

        query = "SELECT * FROM c ORDER BY c._ts DESC OFFSET 0 LIMIT 1"
        items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        return items[0] if items else None

    def get_last_ten_items(self):
       """
        Retrieves the last ten items from the container based on the update or creation time.

        Returns:
            list: A list of the last ten items, where each item is structured as follows:
                - **id** (str): The unique identifier for the item.
                - **user_id** (str): The user associated with the item.
                - **request** (list): A list of request dictionaries containing:
                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.
                - **response** (list): A list of response dictionaries containing:
                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.
                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:
            ```python
            last_ten_items = manager.get_last_ten_items()
            print(last_ten_items)
            ```
        """

       query = "SELECT * FROM c ORDER BY c._ts DESC OFFSET 0 LIMIT 10"
       items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
       return items

    def create_or_update_chat(self, chat_dict):
        """
        Creates or updates an item in the container.

        Args:

            chat_dict (dict): The chat dictionary with the following required structure:
                - **id** (str): The unique identifier for the chat.
                - **user_id** (str): The user associated with the chat.
                - **request** (list): A list of request dictionaries containing:

                    - **content** (str): The content of the request.
                    - **time** (str): The timestamp of the request.
                    - **sentiment** (str): The sentiment of the request.

                - **response** (list): A list of response dictionaries containing:

                    - **content** (str): The content of the response.
                    - **time** (str): The timestamp of the response.
                    - **sentiment** (str): The sentiment of the response.

                - **date** (str): The date of the interaction.
                - **time** (str): The time of the interaction.

        Example:

            chat_dict = {
                "id": "1",
                "user_id": "user123",
                "request": [{"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
                ],
                "response": [{"content": "I'm good, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
                ],
                "date": "2023-11-01",
                "time": "12:01:00"
            }
            manager.create_or_update_chat(chat_dict)
            

        Returns:

            None

        """

        logger.info('\nAMV:APP:Creating or Updating Request Response Pair in DB\n')

        required_keys = ['id', 'user_id', 'request', 'response', 'date', 'time']
        if not all(key in chat_dict for key in required_keys):
            missing_keys = [key for key in required_keys if key not in chat_dict]
            logger.info(f"AMV:APP:chat_dict is missing one or more required keys: {', '.join(missing_keys)}")
            return

        for req in chat_dict['request']:
            if not all(key in req for key in ['content', 'time', 'sentiment']):
                logger.info("AMV:APP:Each request item must contain 'content', 'time', and 'sentiment'")
                return

        for res in chat_dict['response']:
            if not all(key in res for key in ['content', 'time', 'sentiment']):
                logger.info("AMV:APP:Each response item must contain 'content', 'time', and 'sentiment'")
                return

        chat_id = chat_dict["id"]
        try:
            # Try to read the existing chat entry
            existing_chat = self.container.read_item(item=chat_id, partition_key=chat_id)
            # Append the new request and response to the existing lists
            existing_chat["request"].extend(chat_dict["request"])
            existing_chat["response"].extend(chat_dict["response"])
            # Update the chat entry in the database
            self.container.replace_item(item=chat_id, body=existing_chat)
            print("Chat updated successfully")
        except exceptions.CosmosResourceNotFoundError:
            # If the chat entry does not exist, create a new one
            self.container.create_item(body=chat_dict)
            print("Chat created successfully")
        except exceptions.CosmosHttpResponseError as e:
            print(f"An error occurred: {e.message}")

# Example usage
if __name__ == "__main__":

    config = {
        "COSMOS_DB_ENDPOINT": os.getenv("COSMOS_DB_ENDPOINT"),
        "COSMOS_DB_KEY": os.getenv("COSMOS_DB_KEY"),
        "COSMOS_DB_DATABASE_NAME": os.getenv("COSMOS_DB_DATABASE_NAME"),
        "COSMOS_DB_CONTAINER_NAME": os.getenv("COSMOS_DB_CONTAINER_NAME")
    }
    manager = ChatbotDatabaseManager(config=config)
    item = {
        "id": "1",
        "user_id": "user123",
        "request": [
            {"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
        ],
        "response": [
            {"content": "I'm good, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
        ],
        "date": "2023-11-01",
        "time": "12:01:00"
    }
    manager.create_or_update_chat(item)
    read_item = manager.read_item("1")
    print(read_item)
    updated_item = {
        "id": "1",
        "user_id": "user123",
        "request": [
            {"content": "Hello, how are you?", "time": "2023-11-01T12:00:00Z", "sentiment": "positive"}
        ],
        "response": [
            {"content": "I'm great, thank you!", "time": "2023-11-01T12:01:00Z", "sentiment": "positive"}
        ],
        "date": "2023-11-01",
        "time": "12:01:00"
    }
    manager.update_item("1", updated_item)
    

    latest_item = manager.get_latest_item()
    print("Latest item:", latest_item)

    last_ten_items = manager.get_last_ten_items()
    print("Last ten items:", last_ten_items)

    manager.delete_item("1")