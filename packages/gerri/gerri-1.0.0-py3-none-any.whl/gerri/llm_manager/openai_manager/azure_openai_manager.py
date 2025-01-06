from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Suppress httpx INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)

class AzureOpenAIManager:
    """
    A manager class to handle interactions with Azure OpenAI services, including content filtering.

    Config Dict Structure:
        - OPENAI_ENDPOINT (str): The endpoint for the Azure OpenAI service.
        - OPENAI_API_KEY (str): The API key for authentication.
        - OPENAI_DEPLOYMENT_ID (str): The deployment ID for the Azure OpenAI model.
        - OPENAI_API_VERSION (str): The API version to use.
        - TEMPERATURE (float): The temperature parameter for response generation.

    Note:
        Prompt filtering for the following categories has been implemented:
        - Hate
        - Self-harm
        - Sexual content
        - Violence

    If any violations are detected in user inputs or assistant responses, the process halts and returns an error.
    """

    def __init__(self, config={}):
        """
        Initializes the AzureOpenAIManager with environment variables.

        Args:
            config (dict): Configuration options to override environment variables.
        """
        # Reading the environment variables
        self.openai_endpoint = config.get("OPENAI_ENDPOINT", os.getenv("OPENAI_ENDPOINT"))
        self.openai_api_key = config.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
        self.openai_deployment_id = config.get("OPENAI_DEPLOYMENT_ID", os.getenv("OPENAI_DEPLOYMENT_ID"))
        self.api_version = config.get("OPENAI_API_VERSION", os.getenv("OPENAI_API_VERSION"))
        self.temperature = float(config.get("TEMPERATURE", os.getenv("TEMPERATURE")))

        # Initializing OpenAI client
        self.client = AzureOpenAI(
            api_key=self.openai_api_key,
            api_version=self.api_version,
            azure_endpoint=self.openai_endpoint
        )

        self.messages_list = []

    def check_content_filter(self, prompt_filter_results):
        """
        Checks the content filter results for any violations.

        Args:
            prompt_filter_results (list): The content filter results to check.

        Returns:
            tuple: A boolean indicating if it passed, and a list of violations.
        """
        violations = []
        for result in prompt_filter_results:
            if 'content_filter_results' in result:
                filters = result['content_filter_results']
                for category, details in filters.items():
                    if details['filtered']:
                        violations.append(category)

        return len(violations) == 0, violations

    def check_user_input(self, user_input):
        """
        Checks the user input for any violations against content filters.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            tuple: A boolean indicating if it passed, and a list of violations.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.openai_deployment_id,
                messages=[{"role": "user", "content": user_input}],
                temperature=self.temperature,
                stream=False
            )

            if hasattr(response, "prompt_filter_results"):
                return self.check_content_filter(response.prompt_filter_results)
            return True, []
        except Exception as e:
            logging.error("Organization content filter policy breached. Kindly rephrase your message.")
            try:
                # Extract content filter details from error
                if hasattr(e, "response") and e.response:
                    error_data = e.response.json()  # Get JSON error response
                    inner_error = error_data.get("error", {}).get("innererror", {})
                    content_filter_result = inner_error.get("content_filter_result", {})

                    # Collect violations
                    violations = [
                        category for category, details in content_filter_result.items() if details.get("filtered")
                    ]
                    if violations:
                        return False, violations
            except Exception as parse_error:
                logging.error(f"Error parsing content filter result: {parse_error}")

            return False, ["Unknown"]

    def chat_streamed(self, user_input, prompt):
        """
        Streams chat responses from OpenAI.

        Args:
            user_input (str): The user's input message.
            prompt (str): The system prompt to initialize the conversation.

        Yields:
            str: The streamed content of the chat response.
        """
        passed, violations = self.check_user_input(user_input)
        if not passed:
            yield {"error": "Organizations Content Filter Policy Breached. Kindly rephrase your message.", "violations": violations}
            return

        self.messages_list.append({"role": "user", "content": user_input})
        if len(self.messages_list) > 10:
            self.messages_list.pop(0)

        messages = [
            {"role": "system", "content": prompt},
            *self.messages_list
        ]

        for attempt in range(5):
            try:
                response = self.client.chat.completions.create(
                    model=self.openai_deployment_id,
                    messages=messages,
                    temperature=self.temperature,
                    stream=True
                )

                # Check content filter results for assistant's response
                if hasattr(response, "prompt_filter_results"):
                    passed, violations = self.check_content_filter(response.prompt_filter_results)
                    if not passed:
                        yield {"error": "content filter not passed", "violations": violations}
                        return

                for chunk in response:
                    if hasattr(chunk, "choices") and chunk.choices:
                        delta = chunk.choices[0].delta
                        if delta and delta.content:
                            yield delta.content
                        if chunk.choices[0].finish_reason == "stop":
                            return
            except Exception as e:
                logging.error(f"Stream attempt {attempt + 1} failed: {e}")

        yield {"error": "no_response"}

    def chat(self, user_input, prompt):
        """
        Retrieves a complete chat response from OpenAI.

        Args:
            user_input (str): The user's input message.
            prompt (str): The system prompt to initialize the conversation.

        Returns:
            str: The complete chat response.
        """
        passed, violations = self.check_user_input(user_input)
        if not passed:
            return {"error": "Organizations Content Filter Policy Breached. Kindly rephrase your message.", "violations": violations}

        self.messages_list.append({"role": "user", "content": user_input})
        if len(self.messages_list) > 10:
            self.messages_list.pop(0)

        messages = [
            {"role": "system", "content": prompt},
            *self.messages_list
        ]

        for attempt in range(5):
            try:
                response = self.client.chat.completions.create(
                    model=self.openai_deployment_id,
                    messages=messages,
                    temperature=self.temperature
                )

                # Check content filter results for assistant's response
                if hasattr(response, "prompt_filter_results"):
                    passed, violations = self.check_content_filter(response.prompt_filter_results)
                    if not passed:
                        return {"error": "content filter not passed", "violations": violations}

                if response and response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")

        return {"error": "no_response"}

# Example usage
if __name__ == "__main__":
    manager = AzureOpenAIManager()
    prompt = "You are a helpful assistant named Gerri. You are here to assist with any questions or tasks. When asked to introduce yourself simply give your name and that you are an AI assistant for Giant Eagle"

    # Non-streamed example
    user_input = "How are you? Introduce yourself please."
    response = manager.chat(user_input, prompt)
    print("Non-streamed response:", response)

    # Test for content filter fail in non-streamed example
    inappropriate_input = "I would love to have sex with you."
    response = manager.chat(inappropriate_input, prompt)
    print("Non-streamed response (content filter fail test):", response)

    # Streamed example
    print("Streamed response:")
    for chunk in manager.chat_streamed(user_input, prompt):
        print(chunk, end="")

    # Test for content filter fail in streamed example
    print("\nStreamed response (content filter fail test):")
    for chunk in manager.chat_streamed(inappropriate_input, prompt):
        print(chunk, end="")
