import pathlib
import google.generativeai as genai
import psycopg2
import threading

from judge import judge
from huggingface_hub import login

from IPython.display import display
from IPython.display import Markdown

from constants import *

def Gemini():
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
        "temperature": 0.4,
        "top_k": 35,
        "top_p": 0.9,
    }

    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('gemini-pro', safety_settings=safety_settings, generation_config=generation_config)