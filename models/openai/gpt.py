from openai import OpenAI

from constants import OPENAI_API_KEY

class GPT:
    def __init__(self, model_name, temperature, top_p, max_tokens, frequency_penalty, presence_penalty):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model_name = model_name
        # GPT parameters
        self.model_params = {}
        self.model_params["model"] = model_name
        self.model_params["temperature"] = temperature
        self.model_params["top_p"] = top_p
        self.model_params["max_tokens"] = max_tokens
        self.model_params["frequency_penalty"] = frequency_penalty
        self.model_params["presence_penalty"] = presence_penalty
    def generate(self, prompts):
        try:
            response = self.client.chat.completions.create(
                **self.model_params,
                messages=prompts
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f'GPT.generate error: {e}')
        
if __name__ == '__main__':
    gpt = GPT('gpt-3.5-turbo')
    print(gpt.model_name) # Output: 'gpt-3.5-turbo