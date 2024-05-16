from models.gemini.model import Gemini

class LLM:
    def __init__(self) -> None:
        pass
    def generate(prompt) -> str:
        pass

def get_llm_model(name: str) -> LLM:
    match name:
        case 'gemini':
            return Gemini()
        case _:
            raise ValueError(f"unknown model: {name}")
        
class LLMHandler:
    def __init__(self, model: LLM, template: str) -> None:
        self.model = model
        self.template = template
    def make_prompt(self, *kwargs: str) -> str:
        return self.template.format(*kwargs)
    def generate(self, prompt: str) -> str:
        return self.model.generate(prompt)