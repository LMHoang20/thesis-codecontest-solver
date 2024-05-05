from models.gemini.model import Gemini

class LLM:
    def __init__(self) -> None:
        pass
    def generate_content(prompt) -> str:
        pass

def get_llm_model(name: str) -> LLM:
    match name:
        case 'gemini':
            return Gemini()
        case _:
            raise ValueError(f"unknown model: {name}")