import datasets
import psycopg2
from huggingface_hub import login
from constants import *
from transformers import AutoTokenizer, AutoModelForCausalLM

login(HF_READ_TOKEN)

def load_model() -> tuple[AutoModelForCausalLM, AutoTokenizer]:
    model_name = "google/gemma-2b"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def inference(input_text):
    input_ids = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**input_ids, max_new_tokens=2048)
    return tokenizer.decode(outputs[0])

if __name__ == "__main__":
    model, tokenizer = load_model()

    input_text = "Write me a poem about Machine Learning."
    
    print(inference(input_text))
