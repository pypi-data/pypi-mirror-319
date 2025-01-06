'''This module is used to analyze the content safety of the text. 
This includes text that is hateful, self-harm, sexual, or violent.
It also evaluates the text for jailbreak and shield prompt.'''
import os
import requests
import logging
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

logger = logging.getLogger(__name__)

# Sample: Analyze text in sync request
class ContentSafetyManager:
    '''class to analyze the content safety of the text'''
    def __init__(self, config={}):
        '''initialize the content safety manager'''
        load_dotenv()
        self.safety_key = config.get("CONTENT_SAFETY_KEY", os.getenv("CONTENT_SAFETY_KEY")) 
        self.safety_endpoint = config.get("CONTENT_SAFETY_ENDPOINT", os.getenv("CONTENT_SAFETY_ENDPOINT"))

    def analyze_text(self, input_text: str):
        '''analyze the text for content safety for hate sexual violence and self harm
           input is a string
           returns a dictionary with the severity of each category
        '''
        # analyze text
        key = self.safety_key
        endpoint = self.safety_endpoint
        # Create a Content Safety client
        client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        # Construct request
        request = AnalyzeTextOptions(text=input_text)
        # Analyze text
        try:
            response = client.analyze_text(request)
        except HttpResponseError as e:
            logger.info("AMV:APP:Analyze text failed.")
            if e.error:
                logger.info(f"AMV:APP:Error code: {e.error.code}")
                logger.info(f"AMV:APP:Error message: {e.error.message}")
                return {'error':True,'hate': -1, 'self_harm': -1, 'sexual': -1, 'violence': -1}
        hate_result = next(item for item in response.categories_analysis if
                           item.category == TextCategory.HATE)
        self_harm_result = next(item for item in response.categories_analysis if
                                item.category == TextCategory.SELF_HARM)
        sexual_result = next(item for item in response.categories_analysis if
                             item.category == TextCategory.SEXUAL)
        violence_result = next(item for item in response.categories_analysis if
                               item.category == TextCategory.VIOLENCE)
        content_dict={}
        content_dict["hate"]=hate_result.severity
        content_dict["self_harm"]=self_harm_result.severity
        content_dict["sexual"]=sexual_result.severity
        content_dict["violence"]=violence_result.severity
        return content_dict

    def detect_jailbreak(self, text):
        '''
           detect jailbreak in the text
           input is a string
           returns a dictionary with the error status and the severity of the jailbreak
        '''
        api_version = "api-version=2024-02-15-preview"
        url = f"{self.safety_endpoint}/contentsafety/text:detectJailbreak?{api_version}"
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.safety_key,
        }
        data = {
            "text": text
        }
        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code != 200:
            return {'error': True, 'message': 'Invalid response'}
        response_json = response.json()
        response_json['error'] = False
        return response_json

    def shield_prompt(self, user_prompt, documents):
        '''
           shield prompt
           input is the user prompt and the documents
           returns a dictionary with the error status and the response
        '''
        api_version="api-version=2024-02-15-preview"
        url = f"{self.safety_endpoint}/contentsafety/text:shieldPrompt?{api_version}"
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.safety_key,
        }
        data_prompt = {
            "userPrompt": user_prompt,
            "documents": documents
        }
        response = requests.post(url, headers=headers, json=data_prompt, timeout=20)
        if response.status_code != 200:
            return {'error': True, 'message': 'Invalid response'}
        response_json = response.json()
        response_json['error'] = False
        return response_json

if __name__ == "__main__":
    cs=ContentSafetyManager()
    logger.info(cs.analyze_text("please help me"))