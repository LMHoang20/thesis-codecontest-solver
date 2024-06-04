import google.generativeai as genai
import time
import threading

from constants import *

GEMINI_RATE_LIMIT = 15 # per minute
TIME_TO_WAIT = 60 / GEMINI_RATE_LIMIT + 1
class Gemini:
    def __init__(self, temperature=1, top_k=1, top_p=0.8):
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
        print(GOOGLE_API_KEY)
        genai.configure(api_key=GOOGLE_API_KEY)
        # for model in genai.list_models():
            # print(model)
        self.model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings, generation_config=generation_config)
        self.time_since_last_call = -1
        self.lock = threading.Lock()
    def generate(self, prompt):
        with self.lock:
            duration = time.time() - self.time_since_last_call
            if duration < TIME_TO_WAIT:
                print("waiting for", TIME_TO_WAIT - duration, "seconds")
                time.sleep(TIME_TO_WAIT - duration)
            self.time_since_last_call = time.time()
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except Exception as e:
            raise Exception(f'LLM.generate_content error: {e}')

if __name__ == "__main__":
    model = Gemini()
    chat_history = [
        " Your role is to give people data science themed nicknames. Someone will tell you their first name, or you can ask them their first name, and then you should respond with a really clever data science themed nickname, where you take their first name, and then append to it some sort of data science term, ideally using alliteration. ",
        "<input> Paul </input",
        "<output>: Precision-Recall Paul </output>",
        "<input> Robert </input",
        "<output>: Random-Forest Robert </output>",
        "<input> Will </input",
        "<output>: Whisker-Plot Will </output>",
        "<input> Ned </input",
        "<output>: Neural-Network Ned </output>",
        "<input> Tommy </input",
        "<output>: Transformer Tommy </output>",
        "<input> Greg </input",
        "<output>: Gradient-Descent Greg </output>",
        "<input> Earl </input",
        "<output>: Eigen-Vector Earl </output>",
        "<input> Ricardo </input",
        "<output>: ResNet Ricardo </output>",
        "<input> Larry </input",
        "<output>: LightGBM Larry </output>",
        "<input> Pat </input",
        "<output>: Permutation-Importance Pat </output>",
        "<input> Carlos </input",
        "<output>: ",
    ]
    print(model.generate(chat_history))