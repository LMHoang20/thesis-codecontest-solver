import os
from dotenv import load_dotenv

class ConstGetter:
    def __init__(self):
        pass

    @staticmethod
    def get_raw_editorial_urls_path():
        load_dotenv()
        return os.getenv('RAW_EDITORIAL_URLS_PATH')
    
    @staticmethod
    def get_clean_editorial_urls_path():
        load_dotenv()
        return os.getenv('CLEAN_EDITORIAL_URLS_PATH')
    
    @staticmethod
    def get_editorial_content_path():
        load_dotenv()
        return os.getenv('EDITORIAL_CONTENT_PATH')
    
    @staticmethod
    def get_problem_urls_path():
        load_dotenv()
        return os.getenv('PROBLEM_URLS_PATH')
    
    @staticmethod
    def get_hf_read_token():
        load_dotenv()
        return os.getenv('HF_READ_TOKEN')