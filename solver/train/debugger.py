from models import LLM

class Debugger:
    def __init__(self, model: LLM, retry: int):
        self.model = model
        self.retry = retry

    def debug(self, code: str, language: str) -> str:
        for _ in range(self.retry):
            try:
                code = self.model.debug(code, language)
                return code
            except Exception as e:
                pass
        return code