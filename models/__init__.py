from models.gemini.model import Gemini

class LLM:
    def generate(prompt: str) -> str:
        pass

def get_llm_model(name: str) -> LLM:
    match name:
        case 'gemini':
            return Gemini()
        case _:
            raise ValueError(f"unknown model: {name}")