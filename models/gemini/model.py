import google.generativeai as genai
import time
import threading

from constants import *

class Gemini:
    def __init__(self, temperature=0.4, top_k=35, top_p=0.9):
        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        generation_config = {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        }
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings, generation_config=generation_config)
        self.time_since_last_call = time.time()
        self.lock = threading.Lock()
    def generate_content(self, prompt):
        with self.lock:
            duration = time.time() - self.time_since_last_call
            # if duration < 1 seconds, sleep for the remaining time
            if duration < 1:
                time.sleep(1 - duration)
            self.time_since_last_call = time.time()
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except Exception as e:
            raise Exception(f'LLM.generate_content error: {e}')
