from database import get_db_conn
from entity.problem import Problem

phi3_template = \
    "{{ bos_token }}"\
    "{% for message in messages %}"\
        "{% if (message['role'] == 'user') %}"\
            "{{'<|user|>' + '\n' + message['content'] + '<|end|>' + '\n' + '<|assistant|>' + '\n'}}"\
        "{% elif (message['role'] == 'assistant') %}"\
            "{{message['content'] + '<|end|>' + '\n'}}"\
        "{% endif %}"\
    "{% endfor %}"
phi3_template_eos_token = "<|end|>"

def get_problem(offset: int = 0):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.description, p.cf_tags, p.cf_rating, e.content
        FROM problems p JOIN editorials e ON p.name = e.name
        ORDER BY p.name
        LIMIT 1
        OFFSET %s  
    """, (offset,))
    problem = cursor.fetchone()
    cursor.close()
    conn.close()
    if problem is None:
        return None
    return Problem(name = problem[0], description = problem[1], tags = problem[2], rating = problem[3], editorial = problem[4], source="codeforces")

from transformers import AutoTokenizer
import nltk

model_id = "unsloth/Phi-3-mini-4k-instruct-bnb-4bit"
tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="cache-phi-tokenizer")
tokenizer.chat_template = phi3_template

def format_prompt(problem):
    name = problem['name'].strip()
    description = problem['description'].strip()
    tags = problem['tags']
    rating = problem['rating']
    source = problem['source']
    sent_text = nltk.sent_tokenize(problem['editorial'].strip())
    system_turn = f"""
You are an AI assistant specialized in helping student with math and programming problems.
Given a problem, you must come up with a step-by-step solution in natural language to solve the problem.
"""
    user_turn = f"""
Help me solve this problem:
Name: {name}
Source: {source}
Description:
// start of problem description
{description}
// end of problem description
Rating: {rating}
Tags: {tags}
"""
    model_turn = '\n'.join(sent_text)
    return [
        {"role": "system", "content": system_turn},
        {"role": "user", "content": user_turn},
        {"role": "assistant", "content": model_turn},
    ]

offset = 0
while True:
    problem = get_problem(offset)
    if problem is None:
        break
    offset += 1
    problem = problem.to_dict()
    messages = format_prompt(problem)
    prompt = tokenizer.apply_chat_template(messages, tokenize = False, add_generation_prompt = True)
    token_count = len(tokenizer.tokenize(prompt))
    if token_count > 2048:
        continue

import nltk
sent_text = nltk.sent_tokenize(problem['editorial'])
for sentence in sent_text:
    print(sentence)