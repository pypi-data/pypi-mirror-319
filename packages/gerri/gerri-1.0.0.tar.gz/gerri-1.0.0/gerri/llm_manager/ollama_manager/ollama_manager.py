# Description: This file contains the OllamaChat class that is used to interact with the Ollama chat model.
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)

class OllamaChat:
    """
    A class to interact with the Ollama chat model.

    Attributes:
        model (str): The model to use for chat.
        messages (list): A list to store the chat messages.
    """

    def __init__(self, model="llama3.2", temperature=1.0):
        """
        Initializes the OllamaChat with a specified model.

        Args:
            model (str): The model to use for chat. Default is "llama3.2".
        """
        self.model = model
        self.messages = []
        self.temperature = float(temperature)

    def chat(self, user_input):
        """
        Sends a user input to the chat model and streams the response.

        Args:
            user_input (str): The input from the user. Its important to note that the system uses
            the last 10 messages to generate the response. there is hence no need to maintain the
            history for the purposes of the context for this chat.

        Yields:
            str: The content of the response from the chat model.

        Raises:
            Exception: If there is an error in the response.
        """
        #check if messages length is greater than 10. if so, remove the first message
        
        self.messages.append({"role": "user", "content": user_input})
        if len(self.messages) > 10:
            self.messages.pop(0)
        payload = {"model": self.model, "messages": self.messages, "stream": True, "temperature": self.temperature}
        
        r = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json=payload,
            stream=True
        )
        r.raise_for_status()
        output = ""

        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                yield content
                output += content
                # the response streams one token at a time, print that as we receive it

            if body.get("done", False):
                message["content"] = output
                self.messages.append(message)
                return message

    #to be implemented non streaming chat
    def continuous_chat(self):
        """
        Runs the chat interface, prompting the user for input and displaying the response. 
        Exits when the user enters an empty input.
        """
        while True:
            user_input = input("Enter a prompt: ")
            if not user_input:
                exit()
            print()
            for content in chat_instance.chat(user_input):
                print(content, end="")
            print("\n\n")

if __name__ == "__main__":
    chat_instance = OllamaChat()
    chat_instance.continuous_chat()