from dotenv import load_dotenv #this is loading the environment variables
from openai import OpenAI #this is the SDK through which we can chat with openAI directly in Python
import os #OS or operating system package in python helps us achieve os related functions

class OpenAiManager:
    '''class to handle openAI queries'''
    def __init__(self):
        load_dotenv() #here we load environment variables in the .env file. The variable of importance for us is the open AI Key which allows us to chat with openAI safely.
        self.client = OpenAI() #this creates a client which can talk to openAI
    
    def query_openai(self, prompt: str, system_message: str = "You are a helpful assistant for Giant Eagle and your name is EcoQuest. You are a sustainability champion and your mission is to help users construct better prompts so they can try and save energy while using chatGPT responsibly."):
        '''Function to query OpenAI's API'''
        completion = self.client.chat.completions.create( #this function calls allows us ot send a query to openAI and get a response
            model="gpt-4o", # this is the LLM model we use for our answer
            messages=[ #this list is what tells openAi the query to answer
                {"role": "system", "content": system_message}, #role tells openAI what role it is playing.
                {
                    "role": "user", #now as a user you can ask the question listed in content
                    "content": prompt
                }
            ],
            stream=True #this is set to false so that we get the response in one go
        )
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    
    #to be implemented non streaming chat

if __name__ == "__main__":
    query = OpenAiManager()
    for chunk in query.query_openai("What is the best way to save energy when using chatgpt?"):
        print(chunk, end='')  # Print each chunk as it arrives